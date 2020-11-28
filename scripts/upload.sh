#!/bin/bash

# store the original config
cp main.conf main.conf.original

if [ "$SSID" != "" ]; then
  jq ".ssid = \"${SSID}\"" main.conf > tmp
  mv tmp main.conf
else
  echo "SSID env variable is empty which means that no WiFi network identifier is written in the config."
  echo "Your device will not be able to connect to WiFi."
  echo "Please set SSID env variable."
fi

if [ "$WIFI_PASSWORD" != "" ]; then
  jq ".password = \"$WIFI_PASSWORD\"" main.conf > tmp
  mv tmp main.conf
else
  echo "WIFI_PASSWORD env variable is empty which means that no WiFi password is written in the config."
  echo "Your device will not be able to connect to WiFi."
  echo "Please set WIFI_PASSWORD env variable."
fi

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

# restore the original config
mv main.conf.original main.conf
