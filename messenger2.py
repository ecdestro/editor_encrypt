import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter import *
from tkinter import simpledialog
from tkinter import filedialog

def getPass():
    userPass = simpledialog.askstring(title = "Password", prompt = "Enter a password", show = "*")
    return userPass

def getKey():
    seed = getPass()
    password = seed.encode()
    salt = b'0\x9e~\xe0\x98,\xc9\x97\x06\nH\x91r\xb1\xd7\x06\xf4\xaf\xe4\x80t\xa1.8\xb7\xd0\xb15*\xcbA\x93'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=320000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def newFile():
    text.delete(1.0, END)

def openFile():
    location = filedialog.askopenfile(title = "Open", initialdir = ".", defaultextension = "*.txt", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
    try:
        body = location.read().encode()
        cipher = Fernet(getKey())
        decrypted = cipher.decrypt(body)
        text.delete(1.0, END)
        text.insert(1.0, decrypted.decode('utf-8'))
    except AttributeError:
        print("No File Selected")

def saveFile():
    global text
    message = text.get(1.0, END)
    location = filedialog.asksaveasfilename(title = "Save As", initialdir = ".", defaultextension = "*.txt", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
    try:
        body = message.encode()
        cipher = Fernet(getKey())
        encrypted = cipher.encrypt(body)
        file = open(location, "w")
        file.write(encrypted.decode('utf-8'))
        file.close()
    except FileNotFoundError:
        print("No File Selected")

messenger = Tk()
messenger.title("Messenger")
text = Text(messenger)
text.grid()

menuBar = Menu(messenger)
fileMenu = Menu(menuBar, tearoff = False)
fileMenu.add_command(label = "New", command = newFile)
fileMenu.add_command(label = "Open", command = openFile)
fileMenu.add_command(label = "Save As...", command = saveFile)
fileMenu.add_command(label = "Exit", command = messenger.quit)
menuBar.add_cascade(label = "File", menu = fileMenu)

messenger.config(menu = menuBar)
messenger.mainloop()