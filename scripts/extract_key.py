import json
import sys
from rsa import PrivateKey

with open(sys.argv[1], 'rb') as input:
    key = PrivateKey.load_pkcs1(input.read())
    d = {}
    d['n'] = key.n
    d['e'] = key.e
    d['d'] = key.d
    d['p'] = key.p
    d['q'] = key.q
    with open(sys.argv[2], 'w') as output:
        output.write(json.dumps(d))
