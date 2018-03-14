# -*- coding: utf-8 -*-
#!/usr/bin/python 
"""
Created on Thu Feb 22 17:03:26 2018
@author: eards
"""
import socket
import time


port = 21
Host = 'ftp.dlptest.com'#'ftp.mirror.ac.za'  #'127.0.0.1' #''#'ftp://mirror.ac.za/'

ControlSocket = socket.socket()
ControlSocket.connect((Host,port))

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



def ASCII_TypeFileTransferFromServer(Message):#This works 100 % needs exceptions
    
    #dlpuser@dlptest.com
    #eiTqR7EMZD5zy7M
    
    Host,Fileport = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((Host,Fileport))
    
    Message = Message +' cat.jpg'+ '\r\n'
    ControlSocket.send(Message.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))

    with open('TURD.jpg', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            IncommingData.decode('UTF-8')
            File.write(IncommingData)
            print ("File transfer complete")
            File.close()
            FileTransferSocket.close()
            
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))

    return


def ASCII_TypeFileTransferToServer(Message): #This works 100 % needs exceptions
    #
    #dlpuser@dlptest.com
    #eiTqR7EMZD5zy7M
    
    Host,Fileport = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((Host,Fileport))
    
    Message = Message +' cat.jpg'+ '\r\n'
    ControlSocket.send(Message.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))


    File = open('cat.jpg','rb')
    Reading = File.read(8192)
    
    while (Reading):
        
        print('reading file')
        FileTransferSocket.send(Reading.encode('UTF-8'))
        Reading = File.read(8192)  
    print("The file has finnished sending to Server")
    
    File.close()
    FileTransferSocket.close()
    
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))
    
    return

def Login(port,Host): #This is working 100% just maybe some exceptions?
    
    #Establish the connection hopefully receiving the 220 Service Ready
    
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print("Reply from server:\n" + str(Reply))
    
    
    UsernameReplyCode = ''
    while 1:
        
        Username = raw_input("USER ")
        Username = "USER " + Username + '\r\n'
        ControlSocket.send(Username.encode("UTF-8"))
        UsernameReplyCode = ControlSocket.recv(4096).decode("UTF-8")
        print( "Reply from server: \n" + str(UsernameReplyCode))
        
        if UsernameReplyCode[0:3] == '331' or UsernameReplyCode[0:3] =='230':
            break
        
    PassReplyCode =''
    while 1:
        
        Password = raw_input("PASS ")
        Password = "PASS " + Password + '\r\n'
        ControlSocket.send(Password.encode("UTF-8"))
        PassReplyCode = ControlSocket.recv(4096).decode("UTF-8")
        print('Reply from server: \n' + str(PassReplyCode))
        
        if PassReplyCode[0:3] == '230':
            break

    return

def ChangePort(host,port):
    
    #Take text input here from GUI
    host = str(host).replace(".", ",")
    port = hex(port)[2:]
    PortChange = str(host) + "," + str(int(port[0:2],16)) + ","+ str(int(port[2:],16))
    
    Request = 'PORT ' + PortChange + '\r\n'
    
    ControlSocket.send(Request.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    
    print(Reply)
    
    return PortChange

def NoOperation(Message):#This is working 100% just maybe some exceptions?
    
    Message = Message +'\r\n'
    ControlSocket.send(Message.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")

    if Reply[0:3] == '200':
        
        print(Reply)
        
    else:
        
        print ("Something has gone wrong?")
        print(Reply)
    
    return

def List(Message,port,Host):#This is working 100% just maybe some exceptions?
    
    #dlpuser@dlptest.com
    #eiTqR7EMZD5zy7M
    Message = Message + '\r\n'

    Host,Fileport = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((Host,Fileport))
    
    ControlSocket.send(Message.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    
    print('Control connection: \n' + str(Reply))
    
    Reply = FileTransferSocket.recv(4096).decode("UTF-8")
    print('Data port reply:\n ' + str(Reply))
    
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection:\n ' + str(Reply))

    
    return

def passiveMode():#This is working 100% just maybe some exceptions?
    
    Message = 'PASV\r\n'
    ControlSocket.send(Message.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print( '\n' + str(Reply))
    start = Reply.find('(')
    end = Reply.find(')')
    Reply = Reply[start+1:end]
    Reply = Reply.split(',')
    Host = str(Reply[0]) + '.'+ str(Reply[1]) +'.'+ str(Reply[2]) +'.'+ str(Reply[3])
    Port = (int(Reply[4])*256) + int(Reply[5])
    print('New host Data Connection: \n' + str(Host))
    print('New port Data Connection:\n ' + str(Port))
    
    return Host,Port


def CompressionMode():
    
    with open("TEST.txt", "rb") as File:
        
        File = File.read()
        r = ""
        l = len(File)
        
        if l == 0:
            
            return ""
        
        if l == 1:
            
            return File
        
        cnt = 1
        i = 1
        Map = []
        while i < l:
            
            if File[i] == File[i - 1]:
                
                cnt += 1
                
            else:
                
                r = r + File[i - 1] 
                Map.append(cnt)
                cnt = 1
                
            i += 1
            
        r = r + File[i - 1]
        Map.append(cnt)
        print(Map)
        print(r)
        print (len(r))
        counter = 0
        i = 0
        while i <len(r):
            
            if Map[i] == 1:
                
                counter += 1
        
            else:
                print( "counter: " + str(counter))
                if counter > 0 :
                           
                    start = i -counter
                    while counter >= 127:

                     print ("Blocktosend") 
                     print('01111111' + string2bits(r[start:start + 127],8)) 
                     start = start + 127
                     counter = counter - 127
                     
                    if counter > 0 and counter < 127:

                        print ("Blocktosend") 
                        print('0' + Number2bits(counter,7) + string2bits(r[start:start + counter],8)) 
                      
                if Map[i] > 1 and r[i] != ' ':
 
                    NumberBlocks = Map[i] 
                    
                    while NumberBlocks >= 63:
                        
                        print ("Compressed")
                        print('10111111' + str(string2bits(r[i],8)))
                        NumberBlocks = NumberBlocks - 63
                        
                    if NumberBlocks > 0 and NumberBlocks < 63:
                        
                        print ("Compressed")
                        print('10' + Number2bits(NumberBlocks,6) + str(string2bits(r[i],8)))
                        
                if Map[i] > 1 and r[i] == ' ':
                   
                    NumberBlocks = Map[i] 
                    
                    while NumberBlocks >= 63:
                        
                        print ("Compressed space")
                        print('11' + Number2bits(NumberBlocks,6))
                        NumberBlocks = NumberBlocks - 63
                        
                    if NumberBlocks > 0 and NumberBlocks < 63:
                        
                        print ("Compressed space")
                        print('11' + Number2bits(NumberBlocks,6))
                
                counter = 0  
                
            i +=1

        print( "counter: " + str(counter))
        if counter > 0 :
               
            start = i -counter
            print("Start  " + str(start))
            while counter >= 127:
    
             print ("Blocktosend") 
             print('01111111' + string2bits(r[start:start + 127],8)) 
             start = start + 127
             counter = counter - 127
             
            if counter > 0 and counter < 127:
    
                print ("Blocktosend") 
                print('0' + Number2bits(counter,7) + string2bits(r[start:start + counter],8)) 
                      
            
    return

def BlockModeSend(MarkerPosition =0): # Still needs work for the EOR/ERRORs/MArkers
    
    #128 is EOR ----------> No point in this 
    #64 is EOF ----------> done
    #32 is errors -------> no point in this
    #16 marker ---------->done
    
    with open("TEST.txt", "rb") as File:
        
        File = File.read()
        NumberOfBytes = len(File)
        Marker = "rrrrrr"
        
        if MarkerPosition != 0: 
            
            start = MarkerPosition
            
        else:
            
            start = 0


        if NumberOfBytes > 65536:
            end = start + 65536
        else:
            end = NumberOfBytes

        while NumberOfBytes > 65535:
            
            end = start + 65536
            print("Block to send")
            print("000000001111111111111111" + string2bits(str(File[start:end])))
            print("000100000000000000000110" + string2bits(Marker))
            NumberOfBytes - 65535
            start += 65536
            
        if NumberOfBytes > 0 and NumberOfBytes < 65535:
            
            #this must contain the end of file byte
            print("01000000" + Number2bits(NumberOfBytes,16) + string2bits(File[start:end+1]))
        
    return 

def Restart(MarkerPosition):
    
    BlockModeSend(MarkerPosition)
    
    return

    
def string2bits(s='', bitnumer=8):
    
    List = [bin(ord(x))[2:].zfill(bitnumer) for x in s]
    
    return ''.join(List)


def Number2bits(Number, NoBits):
    
    Number = bin(Number)[2:]
    
    return str(Number).zfill(NoBits)



def EDCBIC_TypeFileTransferFromServer(port,Host):
    
    Fileport = port-1
    
    FileTransferSocket = socket.socket()
    FileTransferSocket.connect((Host,Fileport))

    with open('ClientCopy.jpg', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            IncommingData.decode('cp500')
            File.write(IncommingData)
            print ("File transfer complete")
            File.close()
            FileTransferSocket.close()

    return


def EDCBIC_TypeFileTransferToServer(port,host):
    
    FilePort = port-1
    
    FileTransferSocket =socket.socket()
    FileTransferSocket.bind((Host, FilePort)) 
    FileTransferSocket.listen(5)  
    FileTransferConn, FileAddress = FileTransferSocket.accept()
    
    File = open('lol.txt','rb')
    Reading = File.read(8192)
    Reading.encode('cp500')
    
    while (Reading):
             
        FileTransferConn.send(Reading)
        Reading = File.read(8192)
        Reading.encode('cp500')
        
    print("The file has finnished sending to Server")
    
    File.close()
    FileTransferSocket.close()
    
    
    return

def Image_TypeFileTransferToServer(Message):
    
    #Need  to add padding for end of file/record of 000?
    #
    #dlpuser@dlptest.com
    #eiTqR7EMZD5zy7M
    
    Host,Fileport = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((Host,Fileport))
    
    Message = Message +' cat.jpg'+ '\r\n'
    ControlSocket.send(Message.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))


    File = open('cat.jpg','rb')
    Reading = File.read(1)
    
    while (Reading):
        
        print('reading file')
        FileTransferSocket.send(Reading)
        Reading = File.read(1)  
    print("The file has finnished sending to Server")
    
    File.close()
    FileTransferSocket.close()
    
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))

    return


def IMAGE_TypeFileTransferFromServer(Message):
    #Need  to add padding for end of file/record of 000?
    #dlpuser@dlptest.com
    #eiTqR7EMZD5zy7M
    
    Host,Fileport = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((Host,Fileport))
    
    Message = Message +' cat.jpg'+ '\r\n'
    ControlSocket.send(Message.encode("UTF-8"))
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))

    with open('TURD.jpg', 'wb') as File:
        
            print('File opened')
            IncommingData = recv_timeout(FileTransferSocket)
            File.write(IncommingData)
            print ("File transfer complete")
            File.close()
            FileTransferSocket.close()
            
    Reply = ControlSocket.recv(4096).decode("UTF-8")
    print('Control connection reply: \n' + str(Reply))

    return

Login(port,Host)

Message = ''

while 1:
    
    Message = raw_input("Message from client: ")
    
    if Message == 'RETR':
      
          #ASCII_TypeFileTransferFromServer(Message)
          IMAGE_TypeFileTransferFromServer(Message)
          continue
          
    if Message == 'STOR':
        
        #EDCBIC_TypeFileTransferToServer(port,Host)
        #ASCII_TypeFileTransferToServer(Message)
        Image_TypeFileTransferToServer(Message)
        continue
        
    if Message == 'PORT':
        
        Newport = ChangePort('178.21.2.0',7000)
        ControlSocket.send(Newport.encode("UTF-8"))
        continue
    
    if Message == 'NOOP':

        NoOperation(Message)
        continue
    
    if Message == 'REST':
        MarkerPosition =0 # default this to 0
        Restart(MarkerPosition) 
        continue
    
    if Message == 'LIST':
        #LIST [<SP> <pathname>] <CRLF>
        List(Message,port,Host)
        continue
    
    if Message == 'QUIT':
        break
        
    else:
        
        ReceivedData = ControlSocket.recv(4096).decode("UTF-8")
        print ('Received from server: ' + ReceivedData)
        Message = raw_input("Message from client: ")
        
    
ControlSocket.close()