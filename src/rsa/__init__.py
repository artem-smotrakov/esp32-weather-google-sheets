# -*- coding: utf-8 -*-
#
#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""RSA module

Module for calculating large primes, and RSA signing.

WARNING: this implementation does not use compression of the cleartext input to
prevent repetitions, or other common security improvements. Use with care.

"""

from rsa.key import PrivateKey
from rsa.pkcs1 import sign, sign_hash, compute_hash, \
    DecryptionError, VerificationError

__author__ = "Sybren Stuvel, Barry Mead and Yesudeep Mangalapilly"
__date__ = "2018-09-16"
__version__ = '4.0'

__all__ = ['sign', 'compute_hash', 'sign_hash',
           'PrivateKey',
           'DecryptionError', 'VerificationError']
