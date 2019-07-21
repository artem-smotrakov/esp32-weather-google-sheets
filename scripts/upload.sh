#!/bin/bash

# upload code, config and RSA key to esp32
mpfshell \
    -n -c \
    "open ttyUSB0; put main.conf; put key.json; \
    lcd src; mput .*\.py; \
    md rsa; cd rsa; lcd rsa; mput .*\.py; \
    cd ..; md google; cd google; lcd ..; lcd google; mput .*\.py"
