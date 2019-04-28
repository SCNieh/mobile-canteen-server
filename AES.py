import jwt
from Crypto.Cipher import AES

def AES_encrypt(input):
    if len(input) % 16 != 0:
        input += (16 * (len(input) // 16 + 1) - len(input)) * '&'
    obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    return str(obj.encrypt(input))

def encrypt(input):
    encoded_jwt = jwt.encode({'password':input}, 'secret', algorithm='HS256')
    return encoded_jwt.decode('utf-8')

def decrypt(input):
    print(input)
    return jwt.decode(input.encode('utf-8'), 'secret', algorithms=['HS256'])['password']
