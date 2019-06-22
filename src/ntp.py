try:
    import usocket as socket
except:
    import socket

try:
    import ustruct as struct
except:
    import struct

# based on https://github.com/micropython/micropython/blob/master/ports/esp8266/modules/ntptime.py
def time(host = 'pool.ntp.org', port=123):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    NTP_DELTA = 2208988800 # 1970-01-01 00:00:00
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA
