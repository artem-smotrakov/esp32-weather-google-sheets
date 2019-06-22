try:
    import ubinascii as binascii
except:
    import binascii

try:
    import urequests as requests
except:
    import requests

try:
    import ujson as json
except:
    import json

from rsa import pkcs1
import ntp

def encode_dict_to_base64(d):
    return encode_bytes_to_safe_base64(json.dumps(d).encode('utf8'))

def encode_bytes_to_safe_base64(bytes):
    encoded = binascii.b2a_base64(bytes).replace(b'+', b'-')
    return encoded.replace(b'/', b'_').strip().decode('utf8')

# this class builds a JWT to request an access token
# from the Google OAuth 2.0 Authorization Server using a service account
# see https://developers.google.com/identity/protocols/OAuth2ServiceAccount
class JWTBuilder:

    def __init__(self):
        self._header = {}
        self._header['alg'] = 'RS256'
        self._header['typ'] = 'JWT'
        self._claim = {}
        self._claim['iss'] = ''
        self._claim['scope'] = ''
        self._claim['aud'] = 'https://www.googleapis.com/oauth2/v4/token'
        self._claim['exp'] = 0
        self._claim['iat'] = 0
        self._key = None
        self._expiration = 30 * 60 # 30 minutes, in seconds

    def service_account(self, email):
        self._claim['iss'] = email

    # set a space-delimited list of the permissions
    # that the application requests
    def scope(self, value):
        self._claim['scope'] = value

    def key(self, key):
        self._key = key

    # build a JWT
    def build(self):
        print('jwt: build')
        time = ntp.time()
        print('jwt: time: %d' % time)
        self._claim['iat'] = time
        self._claim['exp'] = time + self._expiration
        encoded_header = encode_dict_to_base64(self._header)
        encoded_claim = encode_dict_to_base64(self._claim)
        to_be_signed = '%s.%s' % (encoded_header, encoded_claim)
        print('jwt: signing ...')
        signature = pkcs1.sign(to_be_signed.encode('utf8'), self._key, 'SHA-256')
        print('jwt: done')
        print('jwt: encodeing')
        encoded_signature = encode_bytes_to_safe_base64(signature)
        return '%s.%s' % (to_be_signed, encoded_signature)

class ServiceAccount:

    def __init__(self):
        self._email = ''
        self._scope = ''
        self._key = None

    def email(self, email):
        self._email = email

    def scope(self, scope):
        self._scope = scope

    # set an RSA private key for signing a JWT
    def private_rsa_key(self, key):
        self._key = key

    def token(self):
        print('token: build jwt')

        # prepare a JWT
        builder = JWTBuilder()
        builder.service_account(self._email)
        builder.scope(self._scope)
        builder.key(self._key)
        jwt = builder.build()
        print('token: jwt is done')

        type = 'urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer'
        body = 'grant_type=%s&assertion=%s' % (type, jwt)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post('https://www.googleapis.com/oauth2/v4/token',
                                 data=body,
                                 headers=headers)
        if not response:
            print('token: no response received')

        return response.json()['access_token']
