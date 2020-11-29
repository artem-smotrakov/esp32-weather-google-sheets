import time
import dht
import machine
import util


# this class is a controller that coordinates measurements from multiple sensors
# in a specified interval, it checks a number of sensors and sends the measurements to a handler
class Weather:

    # initializes an instance of Weather with the following parameters
    # - an interval which specifies the schedule for measurements
    # - a handler for handling measurements from sensors
    def __init__(self, interval, handler):
        self.last_measurement = None
        self.interval = util.string_to_millis(interval)
        self.handler = handler
        self.sensors = []

    # add a sensor
    def add(self, sensor):
        self.sensors.append(sensor)

    # checks if it's time to measure
    def check(self):
        current_time = time.ticks_ms()
        deadline = time.ticks_add(self.last_measurement, self.interval)
        if self.last_measurement is None or time.ticks_diff(deadline, current_time) <= 0:
            self.measure()
            self.last_measurement = current_time

    # measure everything and send the measurements to the handler
    def measure(self):
        data = []
        for sensor in self.sensors:
            measurement = sensor.measure()
            data = data + measurement

        if self.handler is not None:
            self.handler.handle(data)


# the class measures temperature and humidity with DHT22 sensor
class DHT22Sensor:

    # initializes a new instance
    def __init__(self, pin):
        self.dht22 = dht.DHT22(machine.Pin(pin))

    # measure temperature and humidity
    def measure(self):
        self.dht22.measure()
        c = self.dht22.temperature()
        h = self.dht22.humidity()
        f = int((c * 1.8) + 32)
        print('centigrade  = %.2f' % c)
        print('farenheit   = %.2f' % f)
        print('humidity    = %.2f' % h)
        return [c, h, f]
