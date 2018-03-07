import Tkinter
import socket

FTPserverPort = 7000
TCPserverPort = 3000
packetSize = 4096

#open(myfile.txt)
#read()

TCPsocket = socket.socket()
TCPsocket.connect(('127.0.0.1',TCPserverPort))
Command = raw_input("Command from client: ")
TCPsocket.send(Command.encode("UTF-8"))

FTPsocket = socket.socket()
FTPsocket.connect(('127.0.0.1',FTPserverPort))
File = raw_input("Request file from server: ")
FTPsocket.send(File.encode("UTF-8"))

#Request sent to server now wait for response
while Command != 'q':
    TCPsocket.send(Command.encode("UTF-8"))
    FTPsocket.send(File.encode("UTF-8"))
    ReceivedData = TCPsocket.recv(packetSize).decode("UTF-8")
    print ('Received from server: ' + ReceivedData)
    Command = raw_input("Command from client: ")
    File = raw_input("Request file from server: ")

FTPsocket.close()
TCPsocket.close()

#top = Tkinter.Tk()
# Code to add widgets will go here...
#top.mainloop()
    

#print("Hello World")