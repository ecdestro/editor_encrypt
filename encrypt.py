from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

print(key)

user = input()

preText = bytes(user, 'utf-8')
cipherText = cipher.encrypt(preText)
print(cipherText)

print(cipher.decrypt(cipherText))
