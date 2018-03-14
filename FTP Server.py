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

def ASCII_TypeFileTransferToClient(port,Host):
    
    FilePort = port-1
    
    FileTransferSocket =socket.socket()
    FileTransferSocket.bind((Host, FilePort)) 
    FileTransferSocket.listen(5)  
    FileTransferConn, FileAddress = FileTransferSocket.accept()
    
    File = open('cat.jpg','rb')
    Reading = File.read(8192)
    
    while (Reading):
             
        FileTransferConn.send(Reading.encode('UTF-8'))
        Reading = File.read(8192)
             
    print("The file has finnished sending to client")
    
    File.close()
    FileTransferSocket.close()
    
    return

def ASCII_TypeFileTransferFromClient(port,Host):
    
    Fileport = port-1
    
    FileTransferSocket = socket.socket()
    FileTransferSocket.connect((Host,Fileport))

    with open('ServerCopy.txt', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            IncommingData.decode('UTF-8')
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


def ChangePort(Newport):
    
    Newport = Newport.split(",")
    Host = ''
    
    for i in range(0,4):
        
        Host+= str(Newport[i])
        if i != 3:
            Host += "."
        
    Port = int(str(hex(int(Newport[4]))[2:])  + str(hex(int(Newport[5]))[2:]),16)
    
    return Host, Port

def NoOperation(Command):
    
    response = "200 OK"
    connection.send(response.encode("UTF-8")) 
    
    return

def EDCBIC_TypeFileTransferToClient(port,Host):
    
    FilePort = port-1
    
    FileTransferSocket =socket.socket()
    FileTransferSocket.bind((Host, FilePort)) 
    FileTransferSocket.listen(5)  
    FileTransferConn, FileAddress = FileTransferSocket.accept()
    
    File = open('cat.jpg', 'rb')
    Reading = File.read(8192)
    Reading.encode('cp500')
    while (Reading):
             
        FileTransferConn.send(Reading)
        Reading = File.read(8192)
        Reading.encode('cp500')
             
    print("The file has finnished sending to client")
    
    File.close()
    FileTransferSocket.close()
    
    return

def EDCBIC_TypeFileTransferFromClient(port,Host):
    
    Fileport = port-1
    
    FileTransferSocket = socket.socket()
    FileTransferSocket.connect((Host,Fileport))

    with open('IBMSHIT.txt', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            IncommingData.decode('cp500')
            File.write(IncommingData)
            print ("File transfer complete")
            File.close()
            FileTransferSocket.close()

    return


def IMAGE_TypeFileTransferFromClient(port,Host):
    
    Fileport = port-1
    
    FileTransferSocket = socket.socket()
    FileTransferSocket.connect((Host,Fileport))

    with open('BINARY.txt', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            File.write(IncommingData)
            print ("File transfer complete")
            File.close()
            FileTransferSocket.close()

    return

def IMAGE_TypeFileTransferToClient(port,Host):
    
    FilePort = port-1
    
    FileTransferSocket =socket.socket()
    FileTransferSocket.bind((Host, FilePort)) 
    FileTransferSocket.listen(5)  
    FileTransferConn, FileAddress = FileTransferSocket.accept()
    
    File = open('TEST.txt','rb')
    Reading = File.read(1)

    while (Reading):
             
        FileTransferConn.send(Reading)
        Reading = File.read(1)
        
    print("The file has finnished sending to Server")
    
    File.close()
    FileTransferSocket.close()

    return
 
    
def CompressionMode():
    
    
    with open('BINARY.txt', 'rb') as File:
        
        File =File.read()
        Binary = File
        LengthOfDAta = len(Binary)
        Header = Binary[0:8]
        Number = 0
        k =0
        
        while 1:
            
            if Header[0] == '1' and Header[1] == '0':

             Number = int(Header[2:],2)

             i =0

             while i < Number:
                 
                 print(chr(int(Binary[k+9:k+16],2)))
                 
                 i += 1
             Number = 1
             
            if Header[0] == '0':
             
             Number = int(Header[1:],2)
             
             print(''.join(chr(int(Binary[i:i+8], 2)) for i in range(k+8, k + Number*8 + 1, 8)))
              
            if Header[0] == '1' and Header[1] == '1':
                
                Number = int(Header[2:],2)
                print(k)
                i =0
                while i<Number:

                    print(chr(int(Binary[k+9:k+16],2)))
                    
                    i += 1
                Number = 0
                
            Header = Binary[k+Number*8 +8 : k+Number*8 + 16] 
            k += Number*8 + 8
            
            if k == LengthOfDAta:
                break
            
    return


def BlockModeReceive(MarkerPosition =0):
    
    #128 is EOR ----------> No point in this 
    #64 is EOF ----------> done
    #32 is errors -------> no point in this
    #16 marker ---------->done

    with open("BINARY.txt", "rb") as File:
        
        File = File.read()
        
        
        if MarkerPosition !=0:
            
            k = MarkerPosition
            Header = File[k:k+24]
            
        else:
            Header = File[0:24]
            k =0
        
        while 1:

            if Header[0:8] == '01000000':
                
                #then it is EOF
                Number = int(Header[8:24],2)
                 
                print(''.join(chr(int(File[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
                
            if Header[0:8] == '00000000':
                
                #There are no EOR/EOF/Errors/Markers
                Number = int(Header[8:24],2)
                print(''.join(chr(int(File[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
            
            if Header[0:8] == '10000000':
                
                Number = int(Header[8:24],2)
                #Suspected errors
            
            if Header[0:8] == '00100000':
                
                Number = int(Header[8:24],2)
                #THere is an EOR
                
            if Header[0:8]== '00010000':
                
                #there are markers
                MarkerPosition = k + Number*8 + 24
                Number = int(Header[8:24],2)
                 
                print(''.join(chr(int(File[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
                
            Header = File[k + Number*8 + 8 : k + Number*8 + 16] 
            k += Number*8 + 24
                
            if k == len(File):
                break
    
    return MarkerPosition

def RestartFileTransfer(MarkerPosition):
    
    
    BlockModeReceive(MarkerPosition)
    
    return


MarkerPosition = BlockModeReceive(MarkerPosition=0)

CompressionMode()
print("lol")
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
        
        ASCII_TypeFileTransferToClient(port,Host)
        continue
    
    if Command == 'STOR':
        #EDCBIC_TypeFileTransferFromClient(port,Host)
        ASCII_TypeFileTransferFromClient(port,Host)
        #IMAGE_TypeFileTransferFromClient(port,Host)
        continue
    
    if Command == 'PORT':
        
        Newport = connection.recv(4096).decode("UTF-8")
        Host, port = ChangePort(Newport) #Should specify host and port for File transfer
        continue
    
    if Command == 'NOOP':
    
        NoOperation(Command)
        continue
    
    if Command == 'REST':
        
        MarkerPosition = 0 #defualt value
        RestartFileTransfer(MarkerPosition) 
        continue
    
    else:
      print(Command) 
      response = (Command + " is not a valid Command")
      connection.send(response.encode("UTF-8")) 
    
    
connection.close()
    