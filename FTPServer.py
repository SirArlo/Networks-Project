import socket

FTPserverPort = 7000
TCPserverPort = 3000
packetSize = 4096

#open(myfile.txt)
#read()

# The 127.0.0.1  IP is for local host and port has been selected as 7000
# Listens for connection with number of backoog connections set to 5
# binds the socket to adress and listens for connections with the arguments of connection and adress bound to socket
TCPsocket =socket.socket()
TCPsocket.bind(('127.0.0.1', TCPserverPort)) 
TCPsocket.listen(5)  
TCPconnection, TCPaddress = TCPsocket.accept()

FTPsocket =socket.socket()
FTPsocket.bind(('127.0.0.1', FTPserverPort)) 
FTPsocket.listen(5)  
FTPconnection, FTPaddress = FTPsocket.accept()

#print ("Connected to socket address"+ address + "and IP "
print ("Connection request from TCP address: " + str(TCPaddress))
print ("Connection request from FTP address: " + str(FTPaddress))
while 1:
    ReceivedFromClientTCP = TCPconnection.recv(4096).decode("UTF-8")
    ReceivedFromClientFTP = FTPconnection.recv(4096).decode("UTF-8")
    if not ReceivedFromClientTCP:
        break
    if not ReceivedFromClientFTP:
        break
    print(ReceivedFromClientTCP)
    print(ReceivedFromClientFTP)
    #response = raw_input("Reply from server: ")
    TCPconnection.send(ReceivedFromClientTCP.encode("UTF-8")) 
    FTPconnection.send(ReceivedFromClientFTP.encode("UTF-8")) 

TCPconnection.close()
FTPconnection.close()