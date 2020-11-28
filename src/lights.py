from machine import Pin


# this class controls LEDs
class Lights:

    # initializes a new instance
    def __init__(self, wifi_led_pin):
        self.wifi_led = Pin(wifi_led_pin, Pin.OUT)

    # turn on the LED for WiFi
    def wifi_on(self):
        self.wifi_led.on()

    # turn off the LED for WiFi
    def wifi_off(self):
        self.wifi_led.off()

    # turn off all LEDs
    def off(self):
        self.wifi_off()
