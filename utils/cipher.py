from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode

class Cipher(object):
    def __init__(self, encoded_key):
        key = RSA.import_key(b64decode(encoded_key.encode('utf-8')))
        self._cipher = PKCS1_OAEP.new(key)

    def encrypt(self, message):
        return b64encode(self._cipher.encrypt(message.encode('utf-8'))).decode('utf-8')

    def decrypt(self, message):
        return self._cipher.decrypt(b64decode(message.encode('utf-8'))).decode('utf-8')
