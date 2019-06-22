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
        self.handler = handler

    # mesures temperature and humidity
    def measure(self):
        self.dht22.measure()
        t = self.dht22.temperature()
        h = self.dht22.humidity()
        if self.handler != None:
            self.handler.handle(t, h)

    # checks if it's time to measure temperature and humidity
    def check(self):
        current_time = time.ticks_ms()
        deadline = time.ticks_add(self.last_measurement, self.interval)
        if time.ticks_diff(deadline, current_time) <= 0:
            self.measure()
            self.last_measurement = current_time
