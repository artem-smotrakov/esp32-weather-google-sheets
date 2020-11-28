#!/bin/bash

# send Ctrl-C
#echo -e '\003' > /dev/ttyUSB0

# upload code, config and RSA key to esp32
mpfshell \
    -n -c \
    "open ttyUSB0; put main.conf; put key.json; \
    lcd src; mput .*\.py; \
    md rsa; cd rsa; mrm .*; lcd rsa; mput .*\.py; \
    cd ..; lcd ..; \
    md google; cd google; mrm .*; lcd google; mput .*\.py; \
    cd ..; lcd ..; \
    md http; cd http; mrm .*; lcd http; mput .*\.py; "
