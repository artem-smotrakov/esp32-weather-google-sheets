# ssid and password for the access point
# make sure that the password is not too short
# otherwise, an OSError occurs while setting up a wi-fi access point
ACCESS_POINT_SSID = 'esp32-dht22-google-sheets'
ACCESS_POINT_PASSWORD = 'helloesp8266'

class WeatherHandler:

    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    def handle(self, t, h):
        print('temperature = %.2f' % t)
        print('humidity    = %.2f' % h)
        spreadsheet.append_values([t, h])

# entry point

# enable garbage collection
import gc
gc.enable()
print('garbage collection threshold: ' + str(gc.threshold()))

from weather import Weather
from config import Config
from machine import Pin
from google.auth import ServiceAccount
from google.sheet import Spreadsheet
import util
import time

# load a config from a file
config = Config('main.conf', 'key.json')

sa = ServiceAccount()
sa.email('esp8266-watering-system@honey-i-am-home.iam.gserviceaccount.com')
sa.scope('https://www.googleapis.com/auth/spreadsheets')
sa.private_rsa_key(config.private_rsa_key())

spreadsheet = Spreadsheet()
spreadsheet.set_service_account(sa)
spreadsheet.set_id('1ntcEW10wqH4FVtfQFL-dbWxvdoweJ-B2NywVgZ9Bb7E')
spreadsheet.set_range('A:A')

weather_handler = WeatherHandler(spreadsheet)

# initialize the DHT22 sensor which measures temperature and humidity
weather = Weather(config.get('dht22_pin'),
                  config.get('measurement_interval'),
                  weather_handler)

# initilize the switch which enables the configuration mode
# if the switch changes its state, then the board is going to reboot immediately
# in order to turn on/off the configuration mode
config_mode_switch = Pin(config.get('config_mode_switch_pin'), Pin.IN)
config_mode_switch.irq(lambda pin: util.reboot())

# first, check if the configuration mode is enabled
# if so, set up an access point, and then start an HTTP server
# the server provides a web form which updates the configuraion of the device
# the server runs on http://192.168.4.1:80
if config_mode_switch.value() == 1:
    from http.server import HttpServer
    from settings import ConnectionHandler
    print('enabled configuration mode')
    access_point = util.start_access_point(ACCESS_POINT_SSID, ACCESS_POINT_PASSWORD)
    handler = ConnectionHandler(config)
    ip = access_point.ifconfig()[0]
    HttpServer(ip, 80, handler).start()
    util.reboot()

# try to connect to wi-fi if the configuraion mode is disabled
util.connect_to_wifi(config.get('ssid'), config.get('password'))

weather_handler.handle(1, 2)

# then, start the main loop
# in the loop, the board is going to check temperature and humidity
while True:
    try:
        weather.check()
    except Exception as e:
        print(e)
    except OSError as e:
        print(e)

    time.sleep(1) # in seconds
