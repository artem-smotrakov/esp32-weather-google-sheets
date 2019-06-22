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

"""Functions for PKCS#1 version 1.5 encryption and signing

This module implements certain functionality from PKCS#1 version 1.5. For a
very clear example, read http://www.di-mgt.com.au/rsa_alg.html#pkcs1schemes

At least 8 bytes of random padding is used when encrypting a message. This makes
these methods much more secure than the ones in the ``rsa`` module.

WARNING: this module leaks information when decryption fails. The exceptions
that are raised contain the Python traceback information, which can be used to
deduce where in the process the failure occurred. DO NOT PASS SUCH INFORMATION
to your users.
"""

try:
    import uhashlib

    HASH_METHODS = {
        'SHA-1': uhashlib.sha1,
        'SHA-256': uhashlib.sha256,
    }
except Exception:
    import hashlib
    HASH_METHODS = {
        'SHA-1': hashlib.sha1,
        'SHA-256': hashlib.sha256,
    }

from rsa import common, transform

# ASN.1 codes that describe the hash algorithm used.
HASH_ASN1 = {
    'SHA-1': b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14',
    'SHA-256': b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20',
}


class CryptoError(Exception):
    """Base class for all exceptions in this module."""


class DecryptionError(CryptoError):
    """Raised when decryption fails."""


class VerificationError(CryptoError):
    """Raised when verification fails."""


def _pad_for_signing(message, target_length):
    r"""Pads the message for signing, returning the padded message.

    The padding is always a repetition of FF bytes.

    :return: 00 01 PADDING 00 MESSAGE

    >>> block = _pad_for_signing(b'hello', 16)
    >>> len(block)
    16
    >>> block[0:2]
    b'\x00\x01'
    >>> block[-6:]
    b'\x00hello'
    >>> block[2:-6]
    b'\xff\xff\xff\xff\xff\xff\xff\xff'

    """

    max_msglength = target_length - 11
    msglength = len(message)

    if msglength > max_msglength:
        raise OverflowError('%i bytes needed for message, but there is only'
                            ' space for %i' % (msglength, max_msglength))

    padding_length = target_length - msglength - 3

    return b''.join([b'\x00\x01',
                     padding_length * b'\xff',
                     b'\x00',
                     message])


def sign_hash(hash_value, priv_key, hash_method):
    """Signs a precomputed hash with the private key.

    Hashes the message, then signs the hash with the given key. This is known
    as a "detached signature", because the message itself isn't altered.

    :param hash_value: A precomputed hash to sign (ignores message). Should be set to
        None if needing to hash and sign message.
    :param priv_key: the :py:class:`rsa.PrivateKey` to sign with
    :param hash_method: the hash method used on the message. Use 'MD5', 'SHA-1',
        'SHA-224', SHA-256', 'SHA-384' or 'SHA-512'.
    :return: a message signature block.
    :raise OverflowError: if the private key is too small to contain the
        requested hash.

    """

    # Get the ASN1 code for this hash method
    if hash_method not in HASH_ASN1:
        raise ValueError('Invalid hash method: %s' % hash_method)
    asn1code = HASH_ASN1[hash_method]

    # Encrypt the hash with the private key
    cleartext = asn1code + hash_value
    keylength = common.byte_size(priv_key.n)
    padded = _pad_for_signing(cleartext, keylength)

    payload = transform.bytes2int(padded)
    encrypted = priv_key.encrypt(payload)
    print('sign_hash: encrypted')
    block = transform.int2bytes(encrypted, keylength)
    print('sign_hash: int2bytes finished')
    
    return block


def sign(message, priv_key, hash_method):
    """Signs the message with the private key.

    Hashes the message, then signs the hash with the given key. This is known
    as a "detached signature", because the message itself isn't altered.

    :param message: the message to sign. Can be an 8-bit string or a file-like
        object. If ``message`` has a ``read()`` method, it is assumed to be a
        file-like object.
    :param priv_key: the :py:class:`rsa.PrivateKey` to sign with
    :param hash_method: the hash method used on the message. Use 'MD5', 'SHA-1',
        'SHA-224', SHA-256', 'SHA-384' or 'SHA-512'.
    :return: a message signature block.
    :raise OverflowError: if the private key is too small to contain the
        requested hash.

    """

    msg_hash = compute_hash(message, hash_method)
    return sign_hash(msg_hash, priv_key, hash_method)


def yield_fixedblocks(infile, blocksize):
    """Generator, yields each block of ``blocksize`` bytes in the input file.

    :param infile: file to read and separate in blocks.
    :param blocksize: block size in bytes.
    :returns: a generator that yields the contents of each block
    """

    while True:
        block = infile.read(blocksize)

        read_bytes = len(block)
        if read_bytes == 0:
            break

        yield block

        if read_bytes < blocksize:
            break


def compute_hash(message, method_name):
    """Returns the message digest.

    :param message: the signed message. Can be an 8-bit string or a file-like
        object. If ``message`` has a ``read()`` method, it is assumed to be a
        file-like object.
    :param method_name: the hash method, must be a key of
        :py:const:`HASH_METHODS`.

    """

    if method_name not in HASH_METHODS:
        raise ValueError('Invalid hash method: %s' % method_name)

    method = HASH_METHODS[method_name]
    hasher = method()

    if hasattr(message, 'read') and hasattr(message.read, '__call__'):
        # read as 1K blocks
        for block in yield_fixedblocks(message, 1024):
            hasher.update(block)
    else:
        # hash the message object itself.
        hasher.update(message)

    return hasher.digest()


__all__ = ['sign',
           'DecryptionError', 'VerificationError', 'CryptoError']
