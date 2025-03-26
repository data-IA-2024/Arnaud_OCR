from cryptography.fernet import Fernet

# we will be encrypting the below string.
message = "hello geeks"

# generate a key for encryption and decryption
# You can use fernet to generate 
# the key or use random key generator
# here I'm using fernet to generate key
def generate_key():
    return Fernet.generate_key().decode()

def encrypt(key,msg):
    fernet = Fernet(key.encode('utf8'))
    return fernet.encrypt(msg.encode()).decode()

def decrypt(key,msg):
    fernet = Fernet(key.encode())
    return fernet.decrypt(msg.encode()).decode()

def verify(key,msg,hash):
    a = encrypt(key, msg)
    print(a)


key = generate_key()
hash = encrypt(key,'1234')
msg = decrypt(key, hash)
print(key,hash, msg)
print(verify(key,msg,hash))

