try:
    import ujson as json
except:
    import json

try:
    import urequests as requests
except:
    import requests

class Spreadsheet:

    def __init__(self):
        self._id = ''
        self._range = ''
        self._url_params = 'insertDataOption=INSERT_ROWS&valueInputOption=RAW'
        self._url_template = 'https://sheets.googleapis.com/v4/spreadsheets/%s/values/%s:append?%s'
        self._sa = None

    def set_id(self, id):
        self._id = id

    def set_range(self, range):
        self._range = range

    def set_service_account(self, sa):
        self._sa = sa

    def append_values(self, values):
        print('spreadsheet: send')

        token = self._sa.token()

        url = self._url_template % (self._id, self._range, self._url_params)
        data = {'values': values}
        headers = {}
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer %s' % token
        response = requests.post(url, json=data, headers=headers)

        if not response:
            print('spreadsheet: no response received')
