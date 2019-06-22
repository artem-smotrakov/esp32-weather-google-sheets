#!/bin/bash

# erase flash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
