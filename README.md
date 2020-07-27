# Weather station based on ESP32 and MicroPython

This is a weather station based on ESP32 and MicroPython.

Here is a list of main features:

*  Measuring temperature and humidity with DHT22 sensor
*  Measuring temperature, humidity and barometric pressure with BME280 sensor
*  Sending data to a Google sheet
*  Supporting Google OAuth 2.0 service to get access to the sheet
*  Configuring the device via web browser

The sheet doesn't need to be publicly available on the Internet. The device doesn't require any middleman such as PushingBox or IFTTT.

Below is a brief description how the project can be built. More details can be found in the following articles:

*  [MicroPython on ESP32: sending data to Google Sheets](https://blog.gypsyengineer.com/en/diy-electronics/micropython-on-esp32-sending-data-to-google-sheets.html)
*  [Weather station based on ESP32 and MicroPython](https://blog.gypsyengineer.com/en/diy-electronics/weather-station-based-on-esp32-and-micropython.html)

## How to make a weather station

Here is a [circuit](circuit/ESP32_weather_station_schem.png) and a [breadboard view](circuit/ESP32_weather_station_bb.png).

The project uses [MicroPython 1.11](https://github.com/micropython/micropython/tree/v1.11). Older or newer versions may also work. The project uses the following tools:

*  `esptool` for flashing ESP32
*  `mpfshell` for uploading files to ESP32
*  `minicom` for connecting to ESP32 for debugging purposes
*  `openssl` and `rsa` package for reading cryptographic keys

### Preparing a service account in Google IAM

To access a Google sheet, the project needs a service account:

*  [Follow the instructions](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) and create a service account
*  Create a key
*  Download a JSON file with the key

The key is encoded in PKCS1 format. Unfortunately the project doesn't support PKCS1 yet. You need to convert the key to the format which the project undrstand:

```
$ cd scripts
$ sh extract_key.sh ../google_key.json ../key.json
```

You'll need `key.json` and an email for the sercvice account.

### Creating a Google sheet

Create a Google sheet and extract its ID from the URL

```
https://docs.google.com/spreadsheets/d/<ID_is_here>/edit#gid=0
```

The following function, when added to the google sheet (Tools > Script editor) allows the
formula uploaded in the `dt` variable (see `measure(self)`) to calculate a local timestamp
from the epoch value loaded in column A of the inserted row

```
function TIMESTAMP_TO_DATE(value) {
  return new Date(value * 1000);
}
```

Share the sheet with your service account. The sheet doesn't need to be publicly accessible from the Internet.

### Preparing a configuration file

`main.conf` contains a configuration for the device. Provide the following parameters:

*  `ssid` and `password` are credentials for your Wi-Fi
*  `google_service_account_email` is an email for the Google's service account
*  `google_sheet_id` is the Google's sheet ID
*  `measurement_interval` is a mesurement interval in `Xh Ym Zs` format, for example, `1h 2m 3s`
*  Pins that are used by switches, sensors, etc. Actual pin numbers may depend on a particular board.
   Mare sure that you update the config to contain right pin numbers for your board.

### Uploading MicroPython

The following scripts may be used to upload MicroPython to ESP32:

```
$ sh scripts/erase.sh
$ sh scripts/flash.sh
$ sh scripts/verify.sh
```

### Uploading code and configs

You can run `sh scripts/upload.sh` to upload the code, the configuration file and the key.

Then, you can connect to the board with `sh scripts/minicon.sh` command to check if everything works fine.

### Configuration mode

The switch turns on the configuration mode. In this mode the device sets up a Wi-Fi access point, and start an HTTP server on http://192.168.4.1. The server provides a web page for updating the configuration of the device.

## Acknowledgement

*  [The implementation of RSA signing](src/rsa) is based on [python-rsa](https://github.com/sybrenstuvel/python-rsa/) package
*  [The implementation of NTP client](src/ntp.py) is based on [ntptime.py](https://github.com/micropython/micropython/blob/master/ports/esp8266/modules/ntptime.py)
*  [The implementation of BME280 micropython driver](src/bme280_int.py) is based on [this](https://github.com/robert-hh/BME280.git)

## Further enhancements

Here is a list of possbile enhancements:

1.  Support [BMP280](https://www.bosch-sensortec.com/bst/products/all_products/bmp280) barometric pressure sensor
1.  Support [DS18B20](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf) temperature sensor
1.  Support [MH-Z19](https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf) CO2 sensor
1.  Support PKCS1
