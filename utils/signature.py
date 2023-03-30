import hashlib
import random
import string

def generate_signature(data, salt):
    return hashlib.sha256(salt + json.dumps(data, sort_keys=True)).hexdigest()

def generate_salt(len=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))