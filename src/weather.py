import time
import dht
import machine
from machine import I2C
import util
from bme280_int import *
# NOTE:  do _not_ issue a "from machine import Pin" statement as that will mess 
# up the of the the variable named "pin"

# the class controls a DHT22 sensor which measures temperature and humidity

class Weather:

    # initilizes an instance of Weather with the following parameters
    # - the dht22_pin for the one-wire DHT22 is connected to
    # - an interval which specifies the schedule for measurements
    # - the bme280_sda_pin for I2C to the BME280 sensor
    # - the bme280_scl_pin for I2C to the BME280 sensor
    # - a handler for handling measured temperature and humidity
    def __init__(self, dht22_pin, bme280_sda_pin, bme280_scl_pin, interval, handler = None):
        self.last_measurement = time.ticks_ms()
        # set up for the DHT22 sensor
        self.dht22 = dht.DHT22(machine.Pin(dht22_pin))
        # set up for the BME280 sensor
        i2c = I2C(sda = machine.Pin(bme280_sda_pin), scl = machine.Pin(bme280_scl_pin))
        self.bme280 = BME280(i2c = i2c)
        # the rest of the init code
        self.interval = util.string_to_millis(interval)
        self.iterations = 0
        self.handler = handler

    # mesures temperature and humidity
    def measure(self):
        # taking readings from the DHT22 sensor
        self.dht22.measure()
        dt    = "=TIMESTAMP_TO_DATE(INDIRECT(\"A\" & ROW()))"
        dht_c = self.dht22.temperature()
        dht_h = self.dht22.humidity()
        dht_f = (dht_c * 1.8) + 32
        # taking readings from the BME280 sensor
        (bme_c, bme_p, bme_h) = self.bme280.read_compensated_data(result = None)
        bme_c = (bme_c / 100)
        bme_f = (bme_c * 1.8) + 32
        bme_p = (bme_p / 256) 
        bme_h = (bme_h / 1024) 
        if self.handler != None:
            self.handler.handle(dt, dht_c, dht_f, dht_h, bme_c, bme_f, bme_p, bme_h)

    # checks if it's time to measure temperature and humidity or
    # initial run (iterations == 0) triggers measure to get initial readings
    def check(self):
        current_time = time.ticks_ms()
        deadline = time.ticks_add(self.last_measurement, self.interval)
        if ((time.ticks_diff(deadline, current_time) <= 0) or (self.iterations == 0)):
            self.measure()
            self.iterations += 1
            self.last_measurement = current_time

# the following function, when added to the google sheet (Tools > Script editor) allows the
# formula uploaded in the "now" variable (see "measure(self)") to calculate a local timestamp
# from the epoch value loaded in column A of the inserted row
#
#function TIMESTAMP_TO_DATE(value) {
#  return new Date(value * 1000);
#}
# see the sheets.py file to set the ValueInputOption to USER_INPUT to avoid now string value being prefixed with a ' 
