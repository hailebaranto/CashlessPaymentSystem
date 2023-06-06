import secrets
import string

def generate_shared_secret():
    alphabet = string.ascii_letters + string.digits
    shared_secret = ''.join(secrets.choice(alphabet) for _ in range(20))
    return shared_secret