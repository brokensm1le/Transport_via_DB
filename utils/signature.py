import hashlib
import random
import string
import time
import json

class SaltSigner(object):
    def generate_salt(self, length):
        return ''.join(self.rand.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))

    def generate_signature(self, data):
        return hashlib.sha256((self._salt + json.dumps(data, sort_keys=True)).encode('utf-8')).hexdigest()

    def __init__(self, salt=None, length=10):
        self.rand = random.Random(int(str(time.time()).replace('.', '')))
        if salt is None:
            salt = self.generate_salt(length)
        self._salt = salt

    def get_salt(self):
        return self._salt
