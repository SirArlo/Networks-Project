# -*- coding: utf-8 -*-
#!/usr/bin/python*-
"""
Created on Sun Mar 04 15:06:43 2018

@author: Arlo
"""

import socket
import os
import time
import random

port = 5000
Host = '127.0.0.1'


##################This works 100%#################### 
def Login(port,Host):
    
    ReceivedUserName = connection.recv(4096).decode("UTF-8")
    ReceivedUserName = formatCommands(ReceivedUserName) 
    ServerFileDirectory = os.path.dirname(os.path.realpath('__file__'))

    while 1:
        
        UserAuthenticate = FolderChecker(ServerFileDirectory,ReceivedUserName)
        
        if UserAuthenticate == 0:
            connection.send('404 User name inccorect!')
            ReceivedUserName = connection.recv(4096).decode("UTF-8")
            ReceivedUserName = formatCommands(ReceivedUserName)
            
        if UserAuthenticate == 1:
            
            UsersFile = os.path.join(ServerFileDirectory, str(ReceivedUserName) +'\credentials.txt')
            RealUsername, RealPassword = readFile(UsersFile)
            break
        
    while 1:
    
        if ReceivedUserName == RealUsername:
            connection.send('331 User name ok, require password')
            break
    
        else:
            connection.send('404 User name inccorect!')
            ReceivedUserName = connection.recv(4096).decode("UTF-8")
            ReceivedUserName = formatCommands(ReceivedUserName)


    ReceivedPassword = connection.recv(4096).decode("UTF-8")
    ReceivedPassword = formatCommands(ReceivedPassword)
 
    while 1:
    
        if ReceivedPassword == RealPassword:
        
            connection.send('230 User logged in, current working directory is /' + str(ReceivedUserName))
            break
    
        else:
            connection.send('404 Password inccorect')
            ReceivedPassword = connection.recv(4096).decode("UTF-8")
            ReceivedPassword = formatCommands(ReceivedPassword)

    return

###########################################################
######################This works 100%####################
def FolderChecker(ServerFileDirectory,ReceivedUserName):
    
    Pathname = (str(ServerFileDirectory) +'\\'+ str(ReceivedUserName))
    IsDirectory =  os.path.isdir(Pathname)
   
    if IsDirectory == True:

      return 1
  
    else:
        
      return 0

###########################################################
######################This works 100%####################
def formatCommands(Message):
    
    CommandsOneParam = ['USER','PASS','RETR','STOR','MKD','RMD','DELE','HELP','LIST','TYPE','MODE','CWD']
    ParameterOne = ''
 
    #Relies on the GUI entering a space after the command
    if Message[0:4] in CommandsOneParam:
        
        #Obtain parameter by including whitespace in the removal
        
        ParameterOne = Message[Message.find(' ') + 1 :]  
        ParameterOne = ParameterOne.replace('\r\n','')

    #Special case for three char commands
    if Message[0:3] in CommandsOneParam:
        
        #Obtain parameter by including whitespace in the removal
        ParameterOne = Message[Message.find(' ') + 1 :]
        ParameterOne = ParameterOne.replace('\r\n','')
        #Format the message to sen to Server
              
    return ParameterOne

###########################################################
######################This works 100%####################
def readFile(filename):
    
    filehandle = open(filename)
    UserName = filehandle.readline().strip()
    Password = filehandle.readline().strip()
    filehandle.close()

    return UserName, Password

###########################################################
######################This works 100%####################
def quitService():
    
    ReplyCode = '221 Thank you come again!'
    connection.send(ReplyCode.encode("UTF-8"))
    print('User ' + str(address)+' has disconnected ')
    
    return

###########################################################
######################This works 100%####################
def SOS(Command):
    
    Parameter = formatCommands(Command)
    
    Parameter = Parameter.upper()
    Filename = str(Parameter) + '.txt'

    with open(Filename,'rb') as HelpFile:
    
        ReplySOS = HelpFile.read()
        connection.send(ReplySOS)
    
        ReplyCode = '214 Help OK'
        connection.send(ReplyCode)
    HelpFile.close()
        

    return



###################################################
##############NEEDS REWRITING######################
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
###################################################
###################################################
    
def getDirectoryList(Command):
    
    #"C:\Users\Arlo\Documents\Repos\Networks project"
    Pathname = formatCommands(Command)
    
    FileList = '\n'  
    ListOfDirFiles = os.listdir(Pathname)
    
    if 'credentials.txt' in ListOfDirFiles:
        ListOfDirFiles = ListOfDirFiles.remove('credentials.txt')  
    
    for i in ListOfDirFiles:
        FileList = FileList + str(i) +'\n'   
        
    DataHost,Dataport = passiveMode(address,Host)
    ReplyCode = '150 opening data connection...'
    
    connection.send(ReplyCode.encode('UTF-8'))
    DataConnection, DataAddress = startDataConnection(DataHost,Dataport)
    
    DataConnection.send(FileList.encode('UTF-8'))
    ReplyCode = '226 Closing data connection'
    
    connection.send(ReplyCode.encode('UTF-8'))
    DataConnection.close()
    
    return


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
    
    Response = "200 OK"
    connection.send(Response.encode("UTF-8")) 
    print('Performed no operation -_- ...')
    
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

##################This Wokrs 98%#################
    
def passiveMode(address,Host):
    
    #this might need port checking

    DataPort = random.sample(range(1024, 5000), 1)
    DataPort = int(DataPort[0])
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    result = sock.connect_ex((address, DataPort))
#    sock.close()
#    
#    if result:
#        print ('Port: ' + str(DataPort) + ' is open' )


    print(DataPort)
    p2 = DataPort % 256
    p1 = (DataPort -p2)/256
    
    print(DataPort)
    print(p1)
    print(p2)
    Host = Host.replace('.',',')
    Message = '227 Entering Passive Mode (' + Host +',' + str(p1) + ',' +str(p2) + ')'
    print(Message)
    connection.send(Message.encode("UTF-8"))

    print('New host Data Connection: \n' + str(Host))
    print('New port Data Connection: \n '+ str(DataPort))
    
    return Host, DataPort

def startDataConnection(Host,port):
    
    FileTransferSocket =socket.socket()
    FileTransferSocket.bind((Host, port))
    FileTransferSocket.listen(5)  
    connection, address = FileTransferSocket.accept() 
    
    return connection, address

def ASCII_TypeFileTransferToClient(Message):
    
    
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



#def makeDirectory(Message):
#    
#    Message,Pathname = formatCommands(Message)
#    
#    ScriptDirectory = os.path.dirname(os.path.realpath(__file__))
#    Pathname = ScriptDirectory + Username
#    os.mkdir(Pathname)
#    
#    
#    
#    return

   
ControlSocket =socket.socket()
ControlSocket.bind((Host, port))
ControlSocket.listen(5)  
connection, address = ControlSocket.accept() 

Initiation = '220 Service established, Welcome to the Silver Server!'
print(Initiation)
connection.send(Initiation.encode("UTF-8"))

Login(port,Host)

print ("Connection request from address: " + str(address))

while 1:
    Command = connection.recv(4096).decode("UTF-8")

    
    if Command[0:4] == 'QUIT':
        quitService()
        break;
        
    if Command[0:4] == 'LIST':
       getDirectoryList(Command)
       continue
   
    if Command[0:4] == 'RETR':
        
        ASCII_TypeFileTransferToClient(port,Host)
        continue
    
    if Command[0:4] == 'STOR':
        #EDCBIC_TypeFileTransferFromClient(port,Host)
        ASCII_TypeFileTransferFromClient(Message)
        #IMAGE_TypeFileTransferFromClient(port,Host)
        continue
    
    if Command[0:4] == 'PORT':
        
        Newport = connection.recv(4096).decode("UTF-8")
        Host, port = ChangePort(Newport) #Should specify host and port for File transfer
        continue
    
    if Command[0:4] == 'NOOP':
    
        NoOperation(Command)
        continue
    
    if Command[0:4] == 'REST':
        
        MarkerPosition = 0 #defualt value
        RestartFileTransfer(MarkerPosition) 
        continue
    
    if Command[0:4] == 'PASV':
      print('in the PASV function')
      Host, port = passiveMode(address,Host)
      continue
  
    if Command[0:4] == 'HELP':
       
       SOS(Command)
       continue
            
    else:
      print(Command) 
      response = (Command + " is not a valid Command")
      connection.send(response.encode("UTF-8")) 
    
    
connection.close()
    