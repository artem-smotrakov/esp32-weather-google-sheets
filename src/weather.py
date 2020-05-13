import time
import dht
import machine
import util

# the class controls a DHT22 sensor which measures temperature and humidity

class Weather:

    # initilizes an instance of Weather with the following parameters
    # - a pin where DHT22 is connected to
    # - an interval which specifies the schedule for measurements
    # - a handler for handling measured temperature and humidity
    def __init__(self, pin, interval, handler = None):
        self.last_measurement = time.ticks_ms()
        self.dht22 = dht.DHT22(machine.Pin(pin))
        self.interval = util.string_to_millis(interval)
        self.iterations = 0
        self.handler = handler

    # mesures temperature and humidity
    def measure(self):
        self.dht22.measure()
        c = self.dht22.temperature()
        h = self.dht22.humidity()
        f = (c * 1.8) + 32
        now = "=TIMESTAMP_TO_DATE(INDIRECT(\"A\" & ROW()))"
        if self.handler != None:
            self.handler.handle(c, f, h, now)

    # checks if it's time to measure temperature and humidity
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
