from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = Fernet(key)

user = input()

bite = bytes(user, 'utf-8')
token = file.encrypt(bite)
print(token)

print(file.decrypt(token))
print(key)