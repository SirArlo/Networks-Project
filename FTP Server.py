# -*- coding: utf-8 -*-
#!/usr/bin/python*-
"""
Created on Sun Mar 04 15:06:43 2018

@author: Arlo
"""

import socket
import os
import time

port = 5000
Host = '127.0.0.1'

def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data=[];
    data='';
     
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(total_data)

def FileTransferToClient(port,Host):
    
    FilePort = port-1
    
    FileTransferSocket =socket.socket()
    FileTransferSocket.bind((Host, FilePort)) 
    FileTransferSocket.listen(5)  
    FileTransferConn, FileAddress = FileTransferSocket.accept()
    
    File = open('cat.jpg','rb')
    Reading = File.read(8192)
    
    while (Reading):
             
        FileTransferConn.send(Reading)
        Reading = File.read(8192)
             
    print("The file has finnished sending to client")
    
    File.close()
    FileTransferSocket.close()
    
    return

def FileTransferFromClient(port,Host):
    
    Fileport = port-1
    
    FileTransferSocket = socket.socket()
    FileTransferSocket.connect((Host,Fileport))

    with open('ServerCopy.jpg', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            File.write(IncommingData)
            print ("File transfer complete")
            File.close()
            FileTransferSocket.close()

    return

def GetDirectoryList(connection):
    
    FileList = '\n'
    list = os.listdir("C:\Users\Arlo\Documents\Repos\Networks project")
       
    for i in list:
        FileList = FileList + str(i) +'\n'   
    connection.send(FileList.encode("UTF-8"))
    
    return

def Login(port,Host):
    
    Username = connection.recv(4096).decode("UTF-8")
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, str(Username) +'/credentials.txt')
    RealUsername, RealPassword = readFile(filename)
    
    while 1:
    
        if Username == RealUsername:
            connection.send('331 User name ok')
            break
    
        else:
            connection.send('404 User name inccorect')
            Username = connection.recv(4096).decode("UTF-8")

    Password = connection.recv(4096).decode("UTF-8")
    
    while 1:
    
        if Password == RealPassword:
        
            connection.send('230 User logged in')
            break
    
        else:
            connection.send('404 Password inccorect')
            Password = connection.recv(4096).decode("UTF-8")

    return

def readFile(filename):
    filehandle = open(filename)
    UserName = filehandle.readline().strip()
    Password = filehandle.readline().strip()
    filehandle.close()

    return UserName, Password


#localhost = '127.0.0.1'
#RIG = '192.168.1.44'
    
ControlSocket =socket.socket()
ControlSocket.bind((Host, port))
ControlSocket.listen(5)  
connection, address = ControlSocket.accept() 

Login(port,Host)

print ("Connection request from address: " + str(address))

while 1:
    Command = connection.recv(4096).decode("UTF-8")
    
    if Command == 'QUIT':
        break;
        
    if Command == 'LIST':
        
       GetDirectoryList(connection)
       continue
   
    if Command == 'RETR':
        
        FileTransferToClient(port,Host)
        continue
    
    if Command == 'STOR':
    
        FileTransferFromClient(port,Host)
        continue
     
    else:
      print(Command) 
      response = (Command + " is not a valid Command")
      connection.send(response.encode("UTF-8")) 
    
    
connection.close()
    