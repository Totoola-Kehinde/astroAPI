import hashlib

def hashpassword(password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password