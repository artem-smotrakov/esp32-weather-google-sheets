#!/bin/bash

# flash esp8266 with specified firmware
esptool.py \
    --chip esp32 \
    --port /dev/ttyUSB0 \
    --baud 460800 \
    write_flash -z 0x1000 esp32-20190529-v1.11.bin
