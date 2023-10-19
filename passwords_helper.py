import re

from cryptography.fernet import Fernet

SYMBOLS = "!@#$%^&*()`<>?|:;,./[]{}=+"

class InvalidPasswordError(Exception):
    def __init__(self, message="Invalid password. Password does not meet the required criteria."):
        self.message = message
        super().__init__(self.message)

def check_pass_complexity(ctx, param, value):
    is_valid = validate_password(value)
    if is_valid:
        return value
    else:
        raise InvalidPasswordError

def validate_password(password):
    if len(password) < 8:
        print("Password is too short!")
        return False
    elif len(password) >= 8 <= 12:
        print("Recommended length is 16+ characters")
    elif len(password) >= 16 <= 128:
        print("It is strong password!")
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        print("Password must contain at least one capital letter")
        return False
    if not re.search("[0-9]", password):
        print("Password must contain at least one digit")
        return False
    for symbol in [*SYMBOLS]:
        symbol_ok = False
        if symbol in password:
            symbol_ok = True
            break
    print("Password must contain at least one special symbol") if not symbol_ok else None
    return True and symbol_ok


def encrypt_password(key, password):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()