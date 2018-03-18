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

#Type List In order ASCII, EDCBIC, IMAGE
TypeList = [True, False, False]

#Mode list in order of Stream, Compressed, Block
ModeList = [True, False, False]

#for using the passive mode or Port mode in that order
PortList = [True,False]

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
        
            connection.send('230 User logged in, current working directory is /')
            break
    
        else:
            connection.send('404 Password inccorect')
            ReceivedPassword = connection.recv(4096).decode("UTF-8")
            ReceivedPassword = formatCommands(ReceivedPassword)
            
    os.chdir((str(ServerFileDirectory) +'\\'+ str(ReceivedUserName)))

    return os.getcwd()

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
    
    CommandsOneParam = ['USER','PASS','RETR','STOR','MKD','RMD','DELE','HELP','LIST','TYPE','MODE','CWD', 'PORT']
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
    Filename = (str(os.path.realpath(__file__)).replace('BAsic TCP Server.py','') + str(Filename))

    with open(Filename,'rb') as HelpFile:
    
        ReplySOS = HelpFile.read()
        connection.send(ReplySOS)
    
        ReplyCode = '214 Help OK'
        connection.send(ReplyCode)
    HelpFile.close()
        

    return

###########################################################
######################This works 100%####################
    
def makeDirectory(Command):
    
    Path = formatCommands(Command)
    FullPath = str(os.getcwd()) + '\\' + str(Path)
    
    if not os.path.exists(FullPath):
        
        os.makedirs(FullPath)
        WorkTree = str(os.getcwd())
        WorkTree = WorkTree.replace(str(UsersDir),'')
        print(WorkTree)
        WorkTree = WorkTree.replace('\\','/')
        print(WorkTree)
        
        ReplyCode = ('227 ' + WorkTree + Path + ' has been created')
        connection.send(ReplyCode.encode('UTF-8'))
        
    else:
        
        ReplyCode = ('550 Requested action not taken, ' + str(Path) + ' already exists')
        connection.send(ReplyCode.encode('UTF-8'))

    return 

###########################################################
######################This works 100%####################
    
def changeWorkingDir(Command):
    
    Path = formatCommands(Command)
    RealPath = Path.replace('/','\\')
    
    try:
        if Path == '/':
            
            os.chdir(UsersDir)
            ReplyCode = ('200 Working directory changed to ' + '/' )
            connection.send(ReplyCode.encode('UTF-8'))

        else:
            
            os.chdir(str(os.getcwd()) + str(RealPath))
            WorkTree = str(os.getcwd())
            WorkTree = WorkTree.replace(str(UsersDir),'')
            WorkTree = WorkTree.replace('\\','/')
            ReplyCode = ('200 Working directory changed to ' + WorkTree )
            connection.send(ReplyCode.encode('UTF-8'))
        
    except OSError:
        
        ReplyCode = '431 No such directory'
        connection.send(ReplyCode.encode('UTF-8'))


    return 

###########################################################
######################This works 100%####################

def removeDirecory(Command):
    
    Path = formatCommands(Command)
    FullPath = ( str(os.getcwd()) + '\\'+ str(Path))
    print('inside the RMD')
    print(FullPath)
    
    try:
        os.rmdir(FullPath)
        ReplyCode = ('250 Requested file action okay' + str(Path) + ' has been removed')
        connection.send(ReplyCode.encode('UTF-8'))
    
    except OSError:
        
        ReplyCode = ('550 Requested action not taken, ' + str(Path) + ' is either not empty or is your current working directory')
        connection.send(ReplyCode.encode('UTF-8'))
        
    return

###########################################################
######################This works 100%####################
    
def changeToParentDir():
    
    os.chdir(UsersDir)
    print(os.getcwd())
    
    ReplyCode = ('200 Working directory changed to ' + '/' )
    connection.send(ReplyCode.encode('UTF-8'))
    
    return 

###########################################################
######################This works 100%####################
    
def deleteFile(Command):
    
    FileName = formatCommands(Command)
    
    try:
        
        os.remove(FileName)
        ReplyCode = ('250 Requested file action okay , ' + str(FileName) + ' has been deleted.')
        connection.send(ReplyCode.encode('UTF-8'))
        
    except OSError:
        
        ReplyCode = ('450 Requested file action not taken, ' + str(FileName) + ' is unavailable or is a path and not a file')
        connection.send(ReplyCode.encode('UTF-8'))
    
    
    return

###########################################################
######################This works 100%####################
def changeType(Command,TypeList):
    
    ParameterOne = formatCommands(Command)

    if ParameterOne == 'A':
        
        ReplyCode = ('200 Command okay, the type has been set to ASCII for the session')
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
            
        TypeList[0] = True
        
    elif ParameterOne == 'E':
        
        ReplyCode = ('200 Command okay, the type has been set to EDCBIC for the session')
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
            
        TypeList[1] = True
         
    elif ParameterOne == 'I':
        
        ReplyCode = ('200 Command okay, the type has been set to Image/Binary for the session')
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
        
        TypeList[2] = True
        
    else:
        ReplyCode = ('500 TYPE ' + ParameterOne + ' is unrecognized or not supported.')
        
  
    connection.send(ReplyCode.encode('UTF-8'))


    return

###########################################################
######################This works 100%####################
def changeMode(Command,ModeList):
    
    ParameterOne = formatCommands(Command)
   
    if ParameterOne == 'S':
        
        ReplyCode = ('200 Command okay, the mode has been set to Stream for the session')
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
            
        ModeList[0] = True

    elif ParameterOne == 'C':
        
        ReplyCode = ('200 Command okay, the mode has been set to Compression for the session')
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
            
        ModeList[1] = True
    
    elif ParameterOne == 'B':
        
        ReplyCode = ('200 Command okay, the mode has been set to Block for the session')
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
        
        ModeList[2] = True
        
    else:
        
        ReplyCode = ('500 MODE ' + ParameterOne + ' is unrecognized or not supported.')
        
        
    connection.send(ReplyCode.encode('UTF-8'))

    return

##########################################################
######################This works 100%####################
    
def NoOperation(Command):
    
    Response = "200 OK"
    connection.send(Response.encode("UTF-8")) 
    print('Performed no operation -_- ...')
    
    return

##########################################################
######################This works 100%####################
def getDirectoryList(Command,UsersDir):
    

    Pathname = formatCommands(Command)

    if Pathname == '/':
        Pathname = ''

    FileList = '\n'  
    
    ListOfDirFiles = os.listdir(str(UsersDir) + str(Pathname))

    if 'credentials.txt' in ListOfDirFiles:
        ListOfDirFiles.remove('credentials.txt')  
        
    sorted(ListOfDirFiles)
    for i in ListOfDirFiles:
        FileList = FileList + str(i) +'\n'   
        
    ReplyCode = '150 opening data connection...' 
    connection.send(ReplyCode.encode('UTF-8'))
      
    DataConnection.send(FileList.encode('UTF-8'))
    ReplyCode = '226 Closing data connection'
    
    connection.send(ReplyCode.encode('UTF-8'))
    DataConnection.shutdown(socket.SHUT_RDWR)
    DataConnection.close()
    
    return

##########################################################
######################This works 100%####################
def passiveMode(Host):
    

    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    FileTransferSocket.bind(('0.0.0.0', 0))
    FileTransferSocket.listen(5)
    DataPort = FileTransferSocket.getsockname()[1]
        

    p2 = DataPort % 256
    p1 = (DataPort -p2)/256

    Host = Host.replace('.',',')
    
    Message = ( '227 Entering Passive Mode (' + Host +',' + str(p1) + ',' +str(p2) + ')' )
    connection.send(Message.encode("UTF-8"))

    DataConnection, DataAddress = FileTransferSocket.accept()

    return DataConnection, DataAddress

##########################################################
######################This works 100%####################
def Store(Command,MarkerPosition=0):
    
    FileName = formatCommands(Command)

    ReplyCode = ('150 File status okay; about to open data connection.')
    connection.send(ReplyCode.encode('UTF-8'))
    
    StartTimer = time.time()

    with open(FileName,'rb') as File:
    
        print(str(FileName) + ' has been opened...')
        
        if ModeList[0] == True:
            OutgoingData = File.read(8192)
             
            while (OutgoingData):
                
                if TypeList[0] == True:
                    OutgoingData.encode('UTF-8')
    
                if TypeList[1] == True:
                    OutgoingData.encode('cp500')
                
                DataConnection.send(OutgoingData)
                OutgoingData = File.read(8192)
                
        if ModeList[1]== True:
            
            sendCompressionMode(DataConnection,File)
        
        if ModeList[2] == True:
            
            sendBlockMode(File,DataConnection,MarkerPosition)
            
            
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print(str(FileName) + ' has been sent to the client in '+ str(ElapsedTime) +' seconds')
        File.close()
        
        ReplyCode = ('226 Closing data connection '+ str(FileName) +' was transferred sucessfully')
        connection.send(ReplyCode.encode('UTF-8'))

    return

##########################################################
######################This works 100%####################
def retrieve(Command):
    
    FileName = formatCommands(Command)
    
    ReplyCode = ('150 File status okay; about to open data connection.')
    connection.send(ReplyCode.encode('UTF-8'))
    
    StartTimer = time.time()
    
    print(FileName)
    print(os.getcwd())

    with open(FileName, 'wb') as File:
        
        if ModeList[0] == True:
            print(str(FileName) + ' has been opened...')
            
            IncommingData = recv_timeout(DataConnection)
            
            if TypeList[0] == True:
                IncommingData.decode('UTF-8')
                File.write(IncommingData)
                
            if TypeList[1] == True:
                IncommingData.decode('cp500')
                File.write(IncommingData)
                
            if TypeList[2] == True:
                File.write(IncommingData)
                
        if ModeList[1]== True:
            
            IncommingData = recv_timeout(DataConnection)
            receiveCompressionMode(DataConnection,IncommingData,File)
        
        if ModeList[2] == True:
            
            IncommingData = recv_timeout(DataConnection)
            receiveBlockMode(File,DataConnection,IncommingData,0)
           
        
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print (str(FileName) + ' has finished downloading\n')
        print(str(FileName) +' ( ' +str(len(IncommingData)/1000) +' kB ) was downloaded in ' +str(ElapsedTime) +' seconds')
        File.close()
        
        ReplyCode = ('226 Closing data connection '+ str(FileName) +' was transferred sucessfully')
        connection.send(ReplyCode.encode('UTF-8'))

    
    return

def string2bits(s='', bitnumer=8):
    
    List = [bin(ord(x))[2:].zfill(bitnumer) for x in s]
    
    return ''.join(List)


def Number2bits(Number, NoBits):
    
    Number = bin(Number)[2:]
    
    return str(Number).zfill(NoBits)

##########################################################
######################This works 100%####################
def printWorkingDir():
    
    WorkTree = str(os.getcwd())
    WorkTree = WorkTree.replace(str(UsersDir),'')
    
    if WorkTree == '':
        WorkTree = '/'
        
    else:
        WorkTree = WorkTree.replace('\\','/')
    
    ReplyCode = ('257 current working directory is ' + WorkTree)
    connection.send(ReplyCode.encode('UTF-8'))
    
    return

##########################################################
######################This works 100%####################
######DO NOT USE FOR ANYHTING OTHER THAN TEXTFILES######
def receiveCompressionMode(DataConnection,IncommingData,File):
    
    Binary = IncommingData
    LengthOfDAta = len(Binary)
    Header = Binary[0:8]
    Number = 0
    k =0
    
    while 1:
        
        if Header[0] == '1' and Header[1] == '0':

         Number = int(Header[2:],2)

         i =0

         while i < Number:
             File.write(chr(int(Binary[k+9:k+16],2)))
             
             i += 1
         Number = 1
         
        if Header[0] == '0':
         
         Number = int(Header[1:],2)
         File.write(''.join(chr(int(Binary[i:i+8], 2)) for i in range(k+8, k + Number*8 + 1, 8)))
          
        if Header[0] == '1' and Header[1] == '1':
            
            Number = int(Header[2:],2)
            i =0
            while i<Number:
                File.write(chr(int(Binary[k+9:k+16],2)))
                
                i += 1
            Number = 0
            
        Header = Binary[k+Number*8 +8 : k+Number*8 + 16] 
        k += Number*8 + 8
        
        if k == LengthOfDAta:
            break
            
    return

##########################################################
######################This works 100%####################
######DO NOT USE FOR ANYHTING OTHER THAN TEXTFILES######
def sendCompressionMode(DataConnection,File):
           
    File = File.read()
    DataToCompress = ''
    l = len(File)
    Iter = 1
    i = 1
    Map = []
    
    while i < l:
        
        if File[i] == File[i - 1]:
            
            Iter += 1
            
        else:
            
            DataToCompress = DataToCompress + File[i - 1] 
            Map.append(Iter)
            Iter = 1
            
        i += 1
        
    DataToCompress = DataToCompress + File[i - 1]
    Map.append(Iter)


    counter = 0
    i = 0
    while i <len(DataToCompress):
        
        if Map[i] == 1:
            
            counter += 1
    
        else:
            
            if counter > 0 :
                       
                start = i -counter
                while counter >= 127:

                 Block  = ('01111111' + string2bits(DataToCompress[start:start + 127],8))
                 
                 if TypeList[0] == True:
                     Block.encode('UTF-8')

                 if TypeList[1] == True:
                    Block.encode('cp500')
                    
                 DataConnection.send(Block)
                 
                 start = start + 127
                 counter = counter - 127
                 
                if counter > 0 and counter < 127:

                    Block = ('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8))            
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    DataConnection.send(Block)
                                       
            if Map[i] > 1:
 
                NumberBlocks = Map[i] 
                
                while NumberBlocks >= 63:
                    
                    Block = ('10111111' + str(string2bits(DataToCompress[i],8)))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    DataConnection.send(Block)
                    NumberBlocks = NumberBlocks - 63
                    
                if NumberBlocks > 0 and NumberBlocks < 63:
                    
                    Block = ('10' + Number2bits(NumberBlocks,6) + str(string2bits(DataToCompress[i],8)))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    DataConnection.send(Block)

            counter = 0  
            
        i +=1
        
 ##############end of while loop##################
 
    if counter > 0 :
           
        start = i -counter
        while counter >= 127:

         Block = ('01111111' + string2bits(DataToCompress[start:start + 127],8)) 

         if TypeList[0] == True:
             Block.encode('UTF-8')

         if TypeList[1] == True:
            Block.encode('cp500')
                    
         DataConnection.send(Block)
         
         start = start + 127
         counter = counter - 127
         
        if counter > 0 and counter < 127:

            Block = ('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8))

            if TypeList[0] == True:
                Block.encode('UTF-8')

            if TypeList[1] == True:
                Block.encode('cp500')
                    
            DataConnection.send(Block)
            
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


#################Needs Testing#####################
###################################################
###################################################

def ChangePort(Command):
    
    Newport = formatCommands(Command)
    Newport = Newport.split(",")
    Host = ''
    
    for i in range(0,4):
        
        Host+= str(Newport[i])
        if i != 3:
            Host += "."
    
    Port = int(str(hex(int(Newport[4]))[2:])  + str(hex(int(Newport[5]))[2:]),16)

    
    ReplyCode = ('200 Command okay, new port is ' + str(Port) +' and new host is ' + str(Host))
    connection.send(ReplyCode.encode('UTF-8'))
    
    ReplyCode = ('150 File status okay; about to open data connection.')
    connection.send(ReplyCode.encode('UTF-8'))
     
     
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    FileTransferSocket.bind((Host,Port))
    FileTransferSocket.listen(5)
    DataConnection, DataAddress = FileTransferSocket.accept()
    
    ReplyCode = ('ohlol')
    DataConnection.send(ReplyCode.encode('UTF-8'))
    
    
    
    return Host, Port

#################Needs Testing#####################
###################################################
###################################################

def RestartFileTransfer(MarkerPosition):
    
    receiveBlockMode(MarkerPosition)

    return


#################Needs Testing#####################
###################################################
###################################################

def sendBlockMode(File,DataConnection,MarkerPosition =0): 
    # Still needs work for the EOR/ERRORs/MArkers
    #128 is EOR ----------> No point in this 
    #64 is EOF ----------> done
    #32 is errors -------> no point in this
    #16 marker ---------->done
    
    File = File.read()
    NumberOfBytes = len(File)
    Marker = 'rrrrrr'
    
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
        Block = ('000000001111111111111111' + string2bits(str(File[start:end])))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        DataConnection.send(Block)

        Block = ('000100000000000000000110' + string2bits(Marker))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        DataConnection.send(Block)
        
        NumberOfBytes - 65535
        start += 65536
        
    if NumberOfBytes > 0 and NumberOfBytes < 65535:
        
        #this must contain the end of file byte
        Block =('01000000' + Number2bits(NumberOfBytes,16) + string2bits(File[start:end+1]))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        DataConnection.send(Block)
    
    return

#################Needs Testing#####################
###################################################
###################################################

def receiveBlockMode(File,DataConnection,IncommingData,MarkerPosition=0):
    #receiveBlockMode(File,DataConnection,IncommingData,MarkerPosition=0):
    #128 is EOR ----------> No point in this 
    #64 is EOF ----------> done
    #32 is errors -------> no point in this
    #16 marker ---------->done
    print('i am receiving blocks?')
    
    if MarkerPosition !=0:
        
        k = MarkerPosition
        Header = IncommingData[k:k+24]
        print('in first check here')
    else:
        Header = IncommingData[0:24]
        k =0
    
    while 1:

        if Header[0:8] == '01000000':
            print('in first if')
            #then it is EOF
            Number = int(Header[8:24],2)
            print(Header[0:8])
            print(Number)
            
            File.write(''.join(chr(int(IncommingData[i:i+8], 2)) for i in range(k + 24, k + Number*8, 8)))
            
            
        if Header[0:8] == '00000000':
            print('in second if')
            #There are no EOR/EOF/Errors/Markers
            Number = int(Header[8:24],2)            
            print(Header[0:8])
            print(Number)
            
            #File.write(''.join(chr(int(IncommingData[i:i+8], 2)) for i in range(k + 24, k + Number*8, 8)))
            File.write(IncommingData[k + 24: k + Number*8])
            
        if Header[0:8]== '00010000':
            print('in third if')
            #there are markers
            MarkerPosition = k + Number*8 + 24
            print(Header[0:8])
            print(Number)
            Number = int(Header[8:24],2)
            
            File.write(''.join(chr(int(IncommingData[i:i+8], 2)) for i in range(k + 24, k + Number*8, 8)))
            
        k = k + Number*8
        Header = IncommingData[k: k + 24] 

        if len(IncommingData) == k:
            print(len(IncommingData))
            print(k)
            print('breaking')
            break

    print('i have finished receiving blocks')
    return MarkerPosition


ControlSocket =socket.socket()
ControlSocket.bind((Host, port))
ControlSocket.listen(5)  
connection, address = ControlSocket.accept() 


Initiation = ('220 Service established, Welcome to the Silver Server!')
connection.send(Initiation.encode("UTF-8"))

UsersDir = Login(port,Host)


print ("Connection request from address: " + str(address))

while 1:
    Command = connection.recv(4096).decode("UTF-8")

    
    if Command[0:4] == 'QUIT':
        quitService()
        break;
        
    if Command[0:4] == 'LIST':

       getDirectoryList(Command,UsersDir)
       continue
   
    if Command[0:4] == 'RETR':
        Store(Command,MarkerPosition=0)
        continue
    
    if Command[0:4] == 'STOR':
        retrieve(Command)
        continue
    
    if Command[0:4] == 'PORT':
        
        ChangePort(Command) 
        continue
    
    if Command[0:4] == 'NOOP':
    
        NoOperation(Command)
        continue
    
    if Command[0:4] == 'REST':
        
        MarkerPosition = 0 #defualt value
        RestartFileTransfer(MarkerPosition) 
        continue
    
    if Command[0:4] == 'PASV':
        
      DataConnection, DataAddress = passiveMode(Host)
      continue
  
    if Command[0:4] == 'HELP':
       
       SOS(Command)
       continue
   
    if Command[0:3] == 'MKD':
        makeDirectory(Command)
        continue
    
    if Command[0:3] == 'RMD':
        removeDirecory(Command)
        continue
    
    if Command[0:3] == 'CWD':
        changeWorkingDir(Command)
        continue
    
    if Command[0:4] == 'CDUP':
        changeToParentDir()
        continue
    
    if Command[0:4] == 'DELE':
        deleteFile(Command)
        continue
    
    if Command[0:4] =='TYPE':
    
        changeType(Command,TypeList)
        continue
    
    if Command[0:4] == 'MODE':
        
        changeMode(Command,ModeList)
        continue
    
    if Command[0:3] == 'PWD':
        printWorkingDir()
        continue
            
    else:
      print(Command) 
      response = ('500 Syntax error, %s unrecognized',Command)
      connection.send(response.encode("UTF-8")) 
    
    
connection.close()
    