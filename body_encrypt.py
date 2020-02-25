from tkinter import *
from tkinter import filedialog
from cryptography.fernet import Fernet

def genKey():
    key = Fernet.generate_key()
    global cipher
    cipher = Fernet(key)
    keyString = key.decode('utf-8')
    keyFile = open("key", "w")
    keyFile.write(keyString)
    keyFile.close()

def newFile():
    genKey()
    text.delete(1.0, END)

def openFile():
    global fileName
    fileName = filedialog.askopenfile(title = "Open", initialdir = ".", defaultextension = "*.txt", filetypes = (("Text files,", "*.txt"), ("All files", "*.*")))
    try:
        body = fileName.read()
        text.delete(1.0, END)
        text.insert(1.0, body)
    except AttributeError:
        print("No File Selected")

def saveAs():
    global text
    body = text.get(1.0, END)
    bodyBytes = bytes(body, 'utf-8')
    encrypted = cipher.encrypt(bodyBytes)
    cipherText = encrypted.decode('utf-8')
    location = filedialog.asksaveasfilename(title = "Save As", initialdir = ".", initialfile = "Untitled", defaultextension = ".txt", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
    try:
        file1 = open(location, "w+")
        file1.write(cipherText)
        file1.close()
    except FileNotFoundError:
        print("No File Selected") 

messenger = Tk()
messenger.title("Messenger")
text = Text(messenger)
text.grid()
newFile()

menuBar = Menu(messenger)
fileMenu = Menu(menuBar, tearoff = False)
fileMenu.add_command(label = "New", command = newFile)
fileMenu.add_command(label = "Open", command = openFile)
fileMenu.add_command(label = "Save As...", command = saveAs)
fileMenu.add_command(label = "Exit", command = messenger.quit)
menuBar.add_cascade(label = "File", menu = fileMenu)

messenger.config(menu=menuBar)
messenger.mainloop()