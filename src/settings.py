# template for an HTTP response which is sent by the server
HTTP_RESPONSE = b"""\
HTTP/1.0 200 OK
Content-Length: %d

%s
"""

# HTTP redirect response which is sent by the server after processing
# data from the form below
HTTP_REDIRECT = b"""\
HTTP/1.0 301 Moved Permanently
Location: /

"""

# an HTML form for configuring the device
FORM_TEMPLATE = """\
<html>
    <head>
        <title>Weather station configuration</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script type="text/javascript">
            function init() {
                var s = document.getElementById('error_handling_options');
                for (var i = 0; i < s.options.length; i++) {
                    if (s.options[i].value == '%error_handling%') {
                        s.options[i].selected = true;
                    }
                }
            }
        </script>
    </head>
    <body onload="init();">
        <h2 style="font-size:10vw">Weather station configuration</h2>
        <form method="post">
            <h3 style="font-size:5vw">Wi-Fi settings</h3>
            <div style="width: 100%;">
                <p style="width: 100%;">SSID:&nbsp;<input name="ssid" type="text" value="%ssid%"/></p>
                <p style="width: 100%;">Password:&nbsp;<input name="password" type="password"/></p>
            </div>
            <h3 style="font-size:5vw">Measurement settings</h3>
            <div style="width: 100%;">
                <p style="width: 100%;">Interval:&nbsp;<input name="measurement_interval" type="text" value="%measurement_interval%"/></p>
            </div>
            <div style="width: 100%;">
                <p style="width: 100%;">CO2 threshold:&nbsp;<input name="co2_threshold" type="text" value="%co2_threshold%"/></p>
            </div>
            <h3 style="font-size:5vw">Google Sheets settings</h3>
            <div style="width: 100%;">
                <p style="width: 100%;">Service account email:&nbsp;
                    <input name="google_service_account_email" type="text" value="%google_service_account_email%" style="width: 100%;"/>
                </p>
                <p style="width: 100%;">Sheet ID:&nbsp;
                    <input name="google_sheet_id" type="text" value="%google_sheet_id%" style="width: 100%;"/>
                </p>
            </div>
            <h3 style="font-size:5vw">Error handling</h3>
            <div style="width: 100%;">
                <p style="width: 100%;">
                    <select name="error_handling" id="error_handling_options">
                        <option value="stop">Stop</option>
                        <option value="reboot">Reboot</option>
                        <option value="ignore">Ignore</option>
                    </select>
                </p>
            </div>
            <div>
                <p style="width: 100%;"><input type="submit" value="Update"></p>
            </div>
        </form>
    </body>
</html>
"""

_hextobyte_cache = None


# borrowed from https://forum.micropython.org/viewtopic.php?t=3076
def unquote(string):
    """unquote('abc%20def') -> b'abc def'."""
    global _hextobyte_cache

    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        return b''

    if isinstance(string, str):
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    # Build cache for hex to char mapping on-the-fly only for codes
    # that are actually used
    if _hextobyte_cache is None:
        _hextobyte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hextobyte_cache.get(code)
            if char is None:
                char = _hextobyte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)


# decode a url-encoded string:
def url_decode(string):
    """url_decode('abc%20def') -> 'abc def'."""
    return unquote(string).decode('utf-8')


# returns an HTTP response with the form above
# the fields in the form contain the current configuration
# (except the password for wi-fi network)
def get_form(config):
    form = FORM_TEMPLATE
    form = form.replace('%ssid%',
                        str(config.get('ssid')))
    form = form.replace('%measurement_interval%',
                        str(config.get('measurement_interval')))
    form = form.replace('%co2_threshold%',
                        str(config.get('co2_threshold')))
    form = form.replace('%error_handling%',
                        str(config.get('error_handling')))
    form = form.replace('%google_service_account_email%',
                        str(config.get('google_service_account_email')))
    form = form.replace('%google_sheet_id%',
                        str(config.get('google_sheet_id')))
    return HTTP_RESPONSE % (len(form), form)


# a handler for incoming HTTP connections
# it prints out the HTML form above,
# and processes the values from the form submitted by a user
# the values are then stored to the configuration
class ConnectionHandler:

    def __init__(self, config, lights):
        self._config = config
        self._lights = lights

    def handle(self, client_s, status_line, headers, data):
        self._lights.error_off()
        try:
            # process data from the web form if a POST request received
            # otherwise, print out the form
            if status_line.startswith('POST') and data:

                # update the config with the data from the form
                params = data.split('&')
                for param in params:
                    parts = param.split('=')
                    name = parts[0].strip()
                    value = parts[1].strip()

                    # don't update the password if the password field is empty
                    if name == 'password' and not value:
                        continue

                    self._config.set(name, url_decode(value))

                # store the config
                self._config.store()

                # redirect the client to avoid resubmitting the form
                client_s.write(HTTP_REDIRECT)
            else:
                client_s.write(get_form(self._config))
        except Exception as e:
            self._lights.error_on()
            print('achtung! something wrong happened!')
            import sys
            sys.print_exception(e)
