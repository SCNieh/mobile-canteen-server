from Crypto.Cipher import AES

s1 = 'This is a key123'
s2 = 'This is an IV456'

def encrypt(input):
    if len(input) % 16 != 0:
        input += (16 * (len(input) // 16 + 1) - len(input)) * '&'
    obj = AES.new(s1, AES.MODE_CBC, s2)
    return obj.encrypt(input)

def decrypt(input):
    obj = AES.new(s1, AES.MODE_CBC, s2)
    result = obj.decrypt(input).decode("utf-8")
    for i in range(len(result) - 1, 0, -1):
        if result[i] != '&':
            break
    return result[:i + 1]
