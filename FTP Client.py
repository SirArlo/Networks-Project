# -*- coding: utf-8 -*-
#!/usr/bin/python 
"""
Created on Thu Feb 22 17:03:26 2018
@author: eards
"""
import socket
import time

port = 5000
Host = '127.0.0.1'

ControlSocket = socket.socket()
ControlSocket.connect((Host,port))

Message = raw_input("Message from client: ")

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



def FileTransferFromServer(port,Host):
    
    Fileport = port-1
    
    FileTransferSocket = socket.socket()
    FileTransferSocket.connect((Host,Fileport))

    with open('ClientCopy.jpg', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            File.write(IncommingData)
            print ("File transfer complete")
            File.close()
            FileTransferSocket.close()

    return


def FileTransferToServer(port,host):
    
    FilePort = port-1
    
    FileTransferSocket =socket.socket()
    FileTransferSocket.bind((Host, FilePort)) 
    FileTransferSocket.listen(5)  
    FileTransferConn, FileAddress = FileTransferSocket.accept()
    
    File = open('car.jpg','rb')
    Reading = File.read(8192)
    
    while (Reading):
             
        FileTransferConn.send(Reading)
        Reading = File.read(8192)
             
    print("The file has finnished sending to Server")
    
    File.close()
    FileTransferSocket.close()
    
    
    return


#get reply and print
#print recv_timeout(TCPsocket)

while Message != 'QUIT':
    
    ControlSocket.send(Message.encode("UTF-8"))
        
    if Message == 'RETR':
      
          FileTransferFromServer(port,Host)
          Message = ''
          
    if Message == 'STOR':
    
        FileTransferToServer(port,Host)
        Message = ''
          
    else:
        ReceivedData = ControlSocket.recv(4096).decode("UTF-8")
        print ('Received from server: ' + ReceivedData)
        Message = raw_input("Message from client: ")
    
ControlSocket.close()