import time
import machine


# reboot the board after some delay (in seconds)
def reboot(delay=5):
    print('rebooting ...')
    time.sleep(delay)
    machine.reset()


# convert time specified in a string to milliseconds
# the format is `Xd Yh Zm Ws` where
#     X is a number of days
#     Y is a number of hours
#     Z is a number of minutes
#     W is a number of seconds
#     all Xd, Yh, Zm and Ws are optional
#
# examples:
#     an empty string is 0 milliseconds
#     `5m` is equal to 5 * 60 * 1000 = 300000 milliseconds
#     `2h 3s` is equal to 2 * 60 * 60 * 1000 + 3 * 1000 =
#                         = 7200000 + 3000 = 7203000 milliseconds
def string_to_millis(string):
    if not string:
        return 0
    value = 0
    for item in string.split(' '):
        item = item.strip()
        l = len(item)
        n = int(item[:l - 1])
        m = item[l - 1]
        if m == 'd':
            value = value + n * 24 * 60 * 60 * 1000
        if m == 'h':
            value = value + n * 60 * 60 * 1000
        if m == 'm':
            value = value + n * 60 * 1000
        if m == 's':
            value = value + n * 1000

    return value
