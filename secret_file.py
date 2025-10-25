import secrets
def get_secret_key():
    return secrets.token_hex(32)
SECRET_KEY = get_secret_key()
print("Secret Key:", SECRET_KEY)