#!/bin/bash

# erase flash
esptool.py --port /dev/ttyUSB0 erase_flash
