from hashlib import sha1
from sage.all import *
from NumTheory import Tonelli_Shank
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode("ascii", errors="replace")

class ECC:
    def __init__(self, a: int, b: int, p: int):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, x: int, y: int) -> bool:
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0

    def __eq__(self, other):
        return (self.a, self.b, self.p) == (other.a, other.b, other.p)


class Point:
    def __init__(self, curve: ECC, x: int = None, y: int = None, is_infinity: bool = False):
        self.curve = curve
        self.x = x
        self.y = y
        self.is_infinity = is_infinity or (x is None and y is None)

    def __str__(self):
        return "Point(Infinity)" if self.is_infinity else f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if self.is_infinity and other.is_infinity:
            return True
        return self.curve == other.curve and self.x == other.x and self.y == other.y

    def __add__(self, other):
        if self.curve != other.curve:
            raise ValueError("Cannot add points from different curves")

        # Identity element handling (Point at Infinity)
        if self.is_infinity:
            return other
        if other.is_infinity:
            return self

        p = self.curve.p
        # P + (-P) = Infinity
        if self.x == other.x and (self.y + other.y) % p == 0:
            return Point(self.curve, is_infinity=True)

        # Standard Doubling Formula
        if self == other:
            slope = (3 * self.x**2 + self.curve.a) * pow(2 * self.y, -1, p) % p
        # Standard Addition Formula
        else:
            slope = (other.y - self.y) * pow(other.x - self.x, -1, p) % p

        # Standard Coordinate Updates
        x3 = (slope**2 - self.x - other.x) % p
        y3 = (slope * (self.x - x3) - self.y) % p

        return Point(self.curve, x3, y3)
    def __mul__(self, n):
        if n ==0:
            return Point(self.curve, is_infinity=True)
        if n ==1:
            return self
        Q = self
        R = Point(self.curve, None,None)
        while n >0:
            if n%2 == 1: R = R+Q
            Q = Q+Q
            n //=2
        return R
    def __rmul__(self,n):
        return self.__mul__(n)
class MontgomeryECC:
    def __init__(self, A: int, B: int, p: int):
        self.A = A
        self.B = B
        self.p = p

    def is_on_curve(self, x: int, y: int) -> bool:
        return (self.B * y**2 - (x**3 + self.A * x**2 + x)) % self.p == 0


class Point:
    def __init__(self, curve: MontgomeryECC, x: int = None, y: int = None, is_infinity: bool = False):
        self.curve = curve
        self.x = x
        self.y = y
        self.is_infinity = is_infinity or (x is None and y is None)

    def __str__(self):
        return "Point(Infinity)" if self.is_infinity else f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if self.is_infinity and other.is_infinity:
            return True
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if self.is_infinity:
            return other
        if other.is_infinity:
            return self

        p = self.curve.p
        A = self.curve.A
        B = self.curve.B

        # P + (-P) = Infinity
        if self.x == other.x and (self.y + other.y) % p == 0:
            return Point(self.curve, is_infinity=True)

        # Montgomery Doubling Formula
        if self == other:
            num = (3 * self.x**2 + 2 * A * self.x + 1) % p
            den = (2 * B * self.y) % p
            slope = (num * pow(den, -1, p)) % p
        # Montgomery Addition Formula
        else:
            num = (other.y - self.y) % p
            den = (other.x - self.x) % p
            slope = (num * pow(den, -1, p)) % p

        # Montgomery Coordinate Updates
        x3 = (B * slope**2 - A - self.x - other.x) % p
        y3 = (slope * (self.x - x3) - self.y) % p

        return Point(self.curve, x3, y3)

    def __mul__(self, n: int):
        if n == 0:
            return Point(self.curve, is_infinity=True)
        if n == 1:
            return self

        R0, R1 = self, self + self
        check_bin = bin(n)[2:]
        for bit in check_bin[1:]:
            if bit == '0':
                R1 = R0 + R1
                R0 = R0 + R0
            else:
                R0 = R0 + R1
                R1 = R1 + R1
        return R0

    def __rmul__(self, n: int):
        return self.__mul__(n)