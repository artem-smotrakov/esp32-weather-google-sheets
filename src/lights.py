from machine import Pin


# this class controls LEDs that report the following:
# - WiFi connection
# - an error
# - High CO2 level
class Lights:

    # initializes a new instance
    def __init__(self, wifi_led_pin, error_led_pin, high_co2_len_pin):
        self.wifi_led = Pin(wifi_led_pin, Pin.OUT)
        self.error_led = Pin(error_led_pin, Pin.OUT)
        self.high_co2_led = Pin(high_co2_len_pin, Pin.OUT)

    # turn on the LED for WiFi
    def wifi_on(self):
        self.wifi_led.on()

    # turn off the LED for WiFi
    def wifi_off(self):
        self.wifi_led.off()

    # turn on the LED that reports an error
    def error_on(self):
        self.error_led.on()

    # turn off the LED that reports an error
    def error_off(self):
        self.error_led.off()

    # turn on the LED that reports high CO2 level
    def high_co2_on(self):
        self.high_co2_led.on()

    # turn off the LED that reports high CO2 level
    def high_co2_off(self):
        self.high_co2_led.off()

    # turn off all LEDs
    def off(self):
        self.wifi_off()
        self.error_off()
        self.high_co2_off()
