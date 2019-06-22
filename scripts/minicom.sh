#!/bin/bash

# press Ctrl-A and then Q to quit minicom

minicom --capturefile=device.log --device /dev/ttyUSB0 -b 115200
