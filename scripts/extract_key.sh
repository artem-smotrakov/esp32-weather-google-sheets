#!/bin/bash

cat ${1} | jq -r .private_key | sed 's/\\n/\n/g' > key.pem
openssl rsa -in key.pem -out rsa_key.pem
python3 extract_key.py rsa_key.pem ${2}

rm -rf key.pem rsa_key.pem > /dev/null 2>&1
