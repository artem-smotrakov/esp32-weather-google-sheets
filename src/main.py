from weather import Weather
from config import Config
from machine import Pin
from google.auth import ServiceAccount
from google.sheet import Spreadsheet
import gc
import time
import util

# ssid and password for the access point which is started in the configuration mode
# make sure that the password is not too short
# otherwise, an OSError occurs while setting up a wi-fi access point
ACCESS_POINT_SSID = 'esp32-weather-google-sheets'
ACCESS_POINT_PASSWORD = 'helloesp32'


# the handle() method below takes temperature and humidity
# and writes them to a spreadsheet
class WeatherHandler:

    def __init__(self, sheet):
        self.sheet = sheet

    def handle(self, c, f, h, now):
        f = int(f)
        print('centigrade  = %.2f' % c)
        print('farenheit   = %.2f' % f)
        print('humidity    = %.2f' % h)
        print('now         = %s' % now)
        self.sheet.append_values([c, f, h, now])


# enable garbage collection
gc.enable()
print('garbage collection threshold: ' + str(gc.threshold()))

# load configuration for a file
config = Config('main.conf', 'key.json')

# create an instance of ServiceAccount class
# which then is going to be used to obtain an OAuth2 token
# for writing data to a sheet
sa = ServiceAccount()
sa.email(config.get('google_service_account_email'))
sa.scope('https://www.googleapis.com/auth/spreadsheets')
sa.private_rsa_key(config.private_rsa_key())

# create an instance of Spreadsheet which is used to write data to a sheet
spreadsheet = Spreadsheet()
spreadsheet.set_service_account(sa)
spreadsheet.set_id(config.get('google_sheet_id'))
spreadsheet.set_range('A:A')

# create a handler which takes temperature and humidity and write them to a sheet
weather_handler = WeatherHandler(spreadsheet)

# initialize the DHT22 sensor which measures temperature and humidity
weather = Weather(config.get('dht22_pin'),
                  config.get('measurement_interval'),
                  weather_handler)

# initialize a switch which turns on the configuration mode
# if the switch changes its state, then the board is going to reboot immediately
config_mode_switch = Pin(config.get('config_mode_switch_pin'), Pin.IN)
config_mode_switch.irq(lambda pin: util.reboot())

# first, check if the configuration mode is enabled
# if so, set up an access point, and then start an HTTP server
# the server provides a web form which updates the configuration of the device
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

# try to connect to wi-fi if the configuration mode is disabled
util.connect_to_wifi(config.get('ssid'), config.get('password'))

# finally, start the main loop
# in the loop, the board is going to check temperature and humidity
while True:
    try:
        weather.check()
    except:
        if config.get('error_handling') == 'reboot':
            print('achtung! something wrong happened! rebooting ...')
            util.reboot()
        elif config.get('error_handling') == 'stop':
            raise
        else:
            print('achtung! something wrong happened! ignoring ...')

    time.sleep(1)  # in seconds

