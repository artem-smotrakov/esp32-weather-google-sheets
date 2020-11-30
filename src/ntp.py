try:
    import usocket as socket
except:
    import socket

try:
    import ustruct as struct
except:
    import struct


# get current time from an NTP server
# based on https://github.com/micropython/micropython/blob/master/ports/esp8266/modules/ntptime.py
def time(host='pool.ntp.org', port=123):
    ntp_query = bytearray(48)
    ntp_query[0] = 0x1b
    ntp_delta = 2208988800  # 1970-01-01 00:00:00
    recipient = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        s.sendto(ntp_query, recipient)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - ntp_delta
