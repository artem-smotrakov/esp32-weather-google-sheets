# Weather station based on ESP32 and MicroPython

This is a weather station based on ESP32 and MicroPython.

Here is a list of main features:

*  Measuring temperature and humidity with DHT22 sensor
*  Measuring CO2 level with MH-Z19B sensor
*  Sending data to a Google sheet
*  Supporting Google OAuth 2.0 service to get access to the sheet
*  Reporting network connection status, errors and high CO2 level with LEDs
*  Configuring the device via web browser

The sheet doesn't need to be publicly available on the Internet. The device doesn't require any middleman such as PushingBox or IFTTT.

This README contains a brief description how the project can be built. More details can be found in the following blogs:

*  [MicroPython on ESP32: sending data to Google Sheets](https://blog.gypsyengineer.com/en/diy-electronics/micropython-on-esp32-sending-data-to-google-sheets.html)
*  [Weather station based on ESP32 and MicroPython](https://blog.gypsyengineer.com/en/diy-electronics/weather-station-based-on-esp32-and-micropython.html)
*  [Measuring CO2 with MH-Z19B on ESP32](https://blog.gypsyengineer.com/en/diy-electronics/measuring-co2-with-mh-z19b-on-esp32.html)

## How to make a weather station

Here is a [circuit](circuit/ESP32_weather_station_1_2_0_schem.png).

The project uses [MicroPython 1.13](https://github.com/micropython/micropython/releases/tag/v1.13). Older or newer versions may also work.
The project uses the following tools:

*  `esptool` for flashing ESP32
*  `mpfshell` for uploading files to ESP32
*  `minicom` for connecting to ESP32 for debugging purposes
*  `openssl` and `rsa` package for reading cryptographic keys

### Preparing a service account in Google IAM

To access a Google sheet, the project needs a service account:

*  [Follow the instructions](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) and create a service account
*  Create a key
*  Download a JSON file with the key

The key is encoded in PKCS1 format. Unfortunately, the project doesn't support PKCS1 yet. You need to convert the key to the format which the project undrstands:

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

Share the sheet with your service account. The sheet doesn't need to be publicly accessible from the Internet.

### Preparing a configuration file

`main.conf` contains a configuration for the device. Provide the following parameters:

*  `ssid` and `password` are credentials for your Wi-Fi
*  `access_point_ssid` and `access_point_password` are credentials for a Wi-Fi access point
    that is started by the device in the configuration mode.
*  `google_service_account_email` is an email for the Google's service account
*  `google_sheet_id` is the Google's sheet ID
*  `measurement_interval` is a mesurement interval in `Xh Ym Zs` format, for example, `1h 2m 3s`
*  `co2_threshold` is a threshold for CO2 level. If the current CO2 level is higher than the threshold,
    the yellow LED turns on.
*   Pins on the ESP32 board that are connected to the sensors, switch and LEDs.

### Uploading MicroPython

The following scripts may be used to upload MicroPython to ESP32:

```
$ sh scripts/erase.sh
$ sh scripts/flash.sh
$ sh scripts/verify.sh
```

### Uploading code and configs

You can run `sh scripts/upload.sh` to upload the code, the configuration file and the key.
Before running the script, set the followin environment variables:

```
$ export SSID=ssid-for-your-wifi
$ export WIFI_PASSWORD=password-for-your-wifi
$ export ACCESS_POINT_SSID=esp32-weather-google-sheets
$ export ACCESS_POINT_PASSWORD=password-for-the-access-point
$ export GOOGLE_SERVICE_ACCOUNT_EMAIL=your-google-service-account-email
$ export GOOGLE_SHEET_ID=your-google-sheet-id
$ sh scripts/upload.sh
```

Then, you can connect to the board with `sh scripts/minicon.sh` command to check if everything works fine.

### Configuration mode

The switch turns on the configuration mode. In this mode the device starts up a Wi-Fi access point, and runs an HTTP server on http://192.168.4.1.
The server provides a web form for updating the configuration of the device.

## Acknowledgement

*  [The implementation of RSA signing](src/rsa) is based on [python-rsa](https://github.com/sybrenstuvel/python-rsa/) package
*  [The implementation of NTP client](src/ntp.py) is based on [ntptime.py](https://github.com/micropython/micropython/blob/master/ports/esp8266/modules/ntptime.py)

## Further enhancements

Here is a list of possbile enhancements:

1.  Support [BMP280](https://www.bosch-sensortec.com/bst/products/all_products/bmp280) barometric pressure sensor
1.  Support [DS18B20](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf) temperature sensor
1.  Support PKCS1
