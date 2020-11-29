from machine import UART
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


# this class measures CO2 with MH-Z19B sensor
class MHZ19BSensor:

    # initializes a new instance
    def __init__(self, tx_pin, rx_pin, lights):
        self.uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=int(tx_pin), rx=int(rx_pin))
        self.lights = lights

    # measure CO2
    def measure(self):
        while True:

            # send a read command to the sensor
            self.uart.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')

            # a little delay to let the sensor measure CO2 and send the data back
            time.sleep(1)  # in seconds

            # read and validate the data
            buf = self.uart.read(9)
            if self.is_valid(buf):
                break

            # retry if the data is wrong
            self.lights.error_on()
            print('error while reading MH-Z19B sensor: invalid data')
            print('retry ...')

        self.lights.error_off()
        co2 = buf[2] * 256 + buf[3]
        print('co2         = %.2f' % co2)
        return [co2]

    # check data returned by the sensor
    def is_valid(self, buf):
        if buf is None or buf[0] != 0xFF or buf[1] != 0x86:
            return False
        i = 1
        checksum = 0x00
        while i < 8:
            checksum += buf[i] % 256
            i += 1
        checksum = ~checksum & 0xFF
        checksum += 1
        return checksum == buf[8]
