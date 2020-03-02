from tkinter import *
from tkinter import filedialog
from cryptography.fernet import Fernet

def genKey():
    key = Fernet.generate_key()
    global cipher
    cipher = Fernet(key)
    keyLocation = filedialog.asksaveasfilename(title = "Save Key As", initialdir = ".")
    try:
        keyFile = open(keyLocation, "w")
        keyFile.write(key.decode('utf-8'))
        keyFile.close()
    except FileNotFoundError:
        print("Key Discarded: ")
        print(key)

def openKey():
    keyFile = filedialog.askopenfile(title = "Open Key File", initialdir = ".")
    try:
        global key
        key = keyFile.read()
        global cipherBytes
        cipherBytes = bytes(key, 'utf-8')
        key = cipherBytes.decode('utf-8')
        global cipher
        cipher = Fernet(cipherBytes)
    except AttributeError:
        print("Key Not Opened")

def newFile():
    genKey()
    text.delete(1.0, END)

def openFile():
    global fileName
    fileName = filedialog.askopenfile(title = "Open", initialdir = ".", defaultextension = "*.txt", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
    body = bytes(fileName.read(), 'utf-8')
    decryptedBody = cipher.decrypt(body)
    text.delete(1.0, END)
    text.insert(1.0, decryptedBody)

def saveAs():
    global text
    body = text.get(1.0, END)
    location = filedialog.asksaveasfilename(title = "Save As", initialdir = ".", initialfile = "Untitled", defaultextension = "*.txt", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
    cipherText = cipher.encrypt(bytes(body, 'utf-8'))
    try:
        file1 = open(location, "w+")
        file1.write(cipherText.decode('utf-8'))
        file1.close()
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
fileMenu.add_command(label = "Save As...", command = saveAs)
fileMenu.add_command(label = "Exit", command = messenger.quit)
keyMenu = Menu(menuBar, tearoff = False)
keyMenu.add_command(label = "Save New Key", command = genKey)
keyMenu.add_command(label = "Open Key", command = openKey)
menuBar.add_cascade(label = "File", menu = fileMenu)
menuBar.add_cascade(label = "Key", menu = keyMenu)
messenger.config(menu = menuBar)
messenger.mainloop()