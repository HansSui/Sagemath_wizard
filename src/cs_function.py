import hashlib
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from typing import Tuple
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

def Floyd_cycle(f, x0):
    tortoise = f(x0)
    hare = f(f(x0))
    while tortoise != hare:
        tortoise= f(tortoise)
        hare = f(f(hare))
    return tortoise. hare
