# Weather station based on ESP32 and Micropython

This is a weater station based on ESP32 and MicroPython.

Here is a list of the main features:

1.  Measure temperature and humidity with DHT22 sensor.
1.  Send data to a Google sheet directly (without any middleman).
1.  Support Google OAuth 2.0 service to get access to the sheet, 
so that the sheet doesn't need to be publicly available on the Internet.
1.  Configure the device via web browser.

## Further enhancements

Here is a list of possbile enhancements:

1.  Support [BMP280](https://www.bosch-sensortec.com/bst/products/all_products/bmp280) barometric pressure sensor.
1.  Support [DS18B20](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf) temperature sensor.
1.  Support [MH-Z19](https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf) CO2 sensor.
