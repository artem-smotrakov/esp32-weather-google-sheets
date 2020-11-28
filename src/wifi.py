import network


# the class starts a WiFi access point
class AccessPoint:

    # initialize a new WiFi access point
    # the constructor takes ssid and password for the access point
    # make sure that the password is not too short
    # otherwise, an OSError may occur while staring the access point
    def __init__(self, access_point_ssid, access_point_password):
        self.access_point_ssid = access_point_ssid
        self.access_point_password = access_point_password
        self.access_point = None

    # start the access point
    def start(self):
        self.access_point = network.WLAN(network.AP_IF)
        self.access_point.active(True)
        self.access_point.config(essid=self.access_point_ssid,
                                 password=self.access_point_password,
                                 authmode=network.AUTH_WPA_WPA2_PSK)

    # returns an IP address of the access point
    def ip(self):
        if self.access_point is None:
            raise Exception('Access point has not started!')
        return self.access_point.ifconfig()[0]
