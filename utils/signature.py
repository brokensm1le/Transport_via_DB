import hashlib
import random
import string
import time

class SaltSigner(object):
    _salt = None
    rand = None

    def generate_salt(self, length):
        return ''.join(self.rand.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))

    def generate_signature(self, data):
        if self._salt is None:
            raise ValueError("No salt provided")
        return hashlib.sha256(self._salt + json.dumps(data, sort_keys=True)).hexdigest()

    def __new__(self, salt=None, length=10):
        self.rand = random.Random(int(str(time.time()).replace('.', '')))
        if salt is None:
            salt = self.generate_salt(self, length)
        self._salt = salt
        return salt, self