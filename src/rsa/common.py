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

"""Common functionality shared by several modules."""


from rsa._compat import is_integer


class NotRelativePrimeError(ValueError):
    def __init__(self, a, b, d, msg=None):
        super(NotRelativePrimeError, self).__init__(
            msg or "%d and %d are not relatively prime, divider=%i" % (a, b, d))
        self.a = a
        self.b = b
        self.d = d


# return the bit size of a non-negative integer
# micropython 1.10 doesn't have int.bit_length() method
# see https://github.com/micropython/micropython/issues/4065
def bit_length(n):
    bits = 0
    while n >> bits:
        bits += 1
    return bits


def bit_size(num):
    """
    Number of bits needed to represent a integer excluding any prefix
    0 bits.

    Usage::

        >>> bit_size(1023)
        10
        >>> bit_size(1024)
        11
        >>> bit_size(1025)
        11

    :param num:
        Integer value. If num is 0, returns 0. Only the absolute value of the
        number is considered. Therefore, signed integers will be abs(num)
        before the number's bit length is determined.
    :returns:
        Returns the number of bits in the integer.
    """

    if num == 0:
        return 0

    if num < 0:
        num = abs(num)

    if not is_integer(num):
        raise TypeError('not integer')

    try:
        return bit_length(num)
    except AttributeError:
        raise TypeError('bit_size(num) only supports integers, not %r' % type(num))


def byte_size(number):
    """
    Returns the number of bytes required to hold a specific long number.

    The number of bytes is rounded up.

    Usage::

        >>> byte_size(1 << 1023)
        128
        >>> byte_size((1 << 1024) - 1)
        128
        >>> byte_size(1 << 1024)
        129

    :param number:
        An unsigned integer
    :returns:
        The number of bytes required to hold a specific long number.
    """
    if number == 0:
        return 1
    return ceil_div(bit_size(number), 8)


def ceil_div(num, div):
    """
    Returns the ceiling function of a division between `num` and `div`.

    Usage::

        >>> ceil_div(100, 7)
        15
        >>> ceil_div(100, 10)
        10
        >>> ceil_div(1, 4)
        1

    :param num: Division's numerator, a number
    :param div: Division's divisor, a number

    :return: Rounded up result of the division between the parameters.
    """
    quanta, mod = divmod(num, div)
    if mod:
        quanta += 1
    return quanta


def extended_gcd(a, b):
    """Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb
    """
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo orignal b
    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    return a, lx, ly  # Return only positive values


def inverse(x, n):
    """Returns the inverse of x % n under multiplication, a.k.a x^-1 (mod n)

    >>> inverse(7, 4)
    3
    >>> (inverse(143, 4) * 143) % 4
    1
    """

    (divider, inv, _) = extended_gcd(x, n)

    if divider != 1:
        raise NotRelativePrimeError(x, n, divider)

    return inv


def modular_pow(base, exponent, modulus):
    if modulus == 1:
        return 0
    # Assert :: (modulus - 1) * (modulus - 1) does not overflow base
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result
