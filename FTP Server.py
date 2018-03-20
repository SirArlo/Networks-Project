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

#Type List In order ASCII, EDCBIC, IMAGE
TypeList = [True, False, False]

#Mode list in order of Stream, Compressed, Block
ModeList = [True, False, False]

#for using the passive mode or Port mode in that order
PortList = [True,False]

##################This works 100%#################### 
def Login(port,Host, Command):
    
    ReceivedUserName = formatCommands(Command) 
    ServerFileDirectory = os.path.dirname(os.path.realpath('__file__'))

    while 1:
        
        UserAuthenticate = FolderChecker(ServerFileDirectory,ReceivedUserName)
        
        if UserAuthenticate == 0:
            connection.send('404 User name inccorect!\r\n')
            ReceivedUserName = connection.recv(4096).decode("UTF-8")
            ReceivedUserName = formatCommands(ReceivedUserName)
            
        if UserAuthenticate == 1:
            print(ReceivedUserName)
            UsersFile = os.path.join(ServerFileDirectory, str(ReceivedUserName) +'\credentials.txt')
            print(ServerFileDirectory)
            print(UsersFile)
            RealUsername, RealPassword = readFile(UsersFile)
            break
        
    while 1:
    
        if ReceivedUserName == RealUsername:
            connection.send('331 User name ok, require password\r\n')
            break
    
        else:
            connection.send('404 User name inccorect!\r\n')
            ReceivedUserName = connection.recv(4096).decode("UTF-8")
            ReceivedUserName = formatCommands(ReceivedUserName)


    ReceivedPassword = connection.recv(4096).decode("UTF-8")
    ReceivedPassword = formatCommands(ReceivedPassword)
 
    while 1:
    
        if ReceivedPassword == RealPassword:
        
            connection.send('230 User logged in, current working directory is / \r\n')
            break
    
        else:
            connection.send('404 Password inccorect\r\n')
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
    
    print(filename)
    
    filehandle = open(filename)
    UserName = filehandle.readline().strip()
    Password = filehandle.readline().strip()
    filehandle.close()

    return UserName, Password

###########################################################
######################This works 100%####################
def quitService():
    
    ReplyCode = '221 Thank you come again!\r\n'
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
    
        ReplyCode = '214 Help OK\r\n'
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
        
        ReplyCode = ('257 "' + WorkTree + Path + '" has been created \r\n')
        connection.send(ReplyCode.encode('UTF-8'))
        
    else:
        
        ReplyCode = ('550 Requested action not taken, ' + Path + ' already exists\r\n')
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
            ReplyCode = ('250 CWD successful "/" is current directory\r\n' )
            connection.send(ReplyCode.encode('UTF-8'))

        else:
            
            os.chdir(str(os.getcwd()) + str(RealPath))
            WorkTree = str(os.getcwd())
            WorkTree = WorkTree.replace(str(UsersDir),'')
            WorkTree = WorkTree.replace('\\','/')
            ReplyCode = ('250 CWD successful."'+ WorkTree+'" is current directory\r\n' )
            connection.send(ReplyCode.encode('UTF-8'))
        
    except OSError:
        
        ReplyCode = '550 Requested action not taken, No such directory\r\n'
        connection.send(ReplyCode.encode('UTF-8'))


    return 

###########################################################
######################This works 100%####################

def removeDirectory(Command):
    
    Path = formatCommands(Command)
    FullPath = ( str(os.getcwd()) + '\\'+ str(Path))

    try:
        os.rmdir(FullPath)
        ReplyCode = ('250 Requested file action okay' + Path  + ' has been removed \r\n')
        connection.send(ReplyCode.encode('UTF-8'))
    
    except OSError:
        
        ReplyCode = ('550 Requested action not taken, ' + Path + ' is not empty\r\n')
        connection.send(ReplyCode.encode('UTF-8'))
        
    return

###########################################################
######################This works 100%####################
    
def changeToParentDir():
    
    os.chdir(UsersDir)
    print(os.getcwd())
    
    ReplyCode = ('200 Working directory changed to / \r\n' )
    connection.send(ReplyCode.encode('UTF-8'))
    
    return 

###########################################################
######################This works 100%####################
    
def deleteFile(Command):
    
    FileName = formatCommands(Command)
    
    try:
        
        os.remove(FileName)
        ReplyCode = ('250 Requested file action okay , ' + FileName+ ' has been deleted.\r\n')
        connection.send(ReplyCode.encode('UTF-8'))
        
    except OSError:
        
        ReplyCode = ('450 Requested file action not taken, ' + FileName + ' is not a file\r\n')
        connection.send(ReplyCode.encode('UTF-8'))
    
    
    return

###########################################################
######################This works 100%####################
def changeType(Command,TypeList):
    
    ParameterOne = formatCommands(Command)

    if ParameterOne == 'A':
        
        ReplyCode = ('200 Command okay, the type has been set to ASCII for the session\r\n')
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
            
        TypeList[0] = True
        
    elif ParameterOne == 'E':
        
        ReplyCode = ('200 Command okay, the type has been set to EDCBIC for the session\r\n')
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
            
        TypeList[1] = True
         
    elif ParameterOne == 'I':
        
        ReplyCode = ('200 Command okay, the type has been set to Image/Binary for the session\r\n')
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
        
        TypeList[2] = True
        
    else:
        ReplyCode = ('500 TYPE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
        
  
    connection.send(ReplyCode.encode('UTF-8'))


    return

###########################################################
######################This works 100%####################
def changeMode(Command,ModeList):
    
    ParameterOne = formatCommands(Command)
   
    if ParameterOne == 'S':
        
        ReplyCode = ('200 Command okay, the mode has been set to Stream for the session\r\n')
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
            
        ModeList[0] = True

    elif ParameterOne == 'C':
        
        ReplyCode = ('200 Command okay, the mode has been set to Compression for the session\r\n')
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
            
        ModeList[1] = True
    
    elif ParameterOne == 'B':
        
        ReplyCode = ('200 Command okay, the mode has been set to Block for the session\r\n')
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
        
        ModeList[2] = True
        
    else:
        
        ReplyCode = ('500 MODE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
        
        
    connection.send(ReplyCode.encode('UTF-8'))

    return

##########################################################
######################This works 100%####################
    
def NoOperation(Command):
    
    Response = "200 OK\r\n"
    connection.send(Response.encode("UTF-8")) 
    print('Performed no operation -_- ...')
    
    return

##########################################################
######################This works 100%####################
def getDirectoryList(Command,UsersDir,DataConnection):
    

    Pathname = formatCommands(Command)

    if Pathname == 'LIST':
        Pathname = '\\'
        
    if Pathname == '/':
        Pathname = ''

    FileList = '\n'  
    
    ListOfDirFiles = os.listdir(str(UsersDir) + str(Pathname))

    if 'credentials.txt' in ListOfDirFiles:
        ListOfDirFiles.remove('credentials.txt')  
        
    sorted(ListOfDirFiles)
    for i in ListOfDirFiles:
        FileList = FileList + str(i) +'\n'   
          
    DataConnection.send(FileList.encode('UTF-8'))
    
    WorkTree = str(os.getcwd())
    WorkTree = WorkTree.replace(str(UsersDir),'')
    WorkTree = WorkTree.replace('\\','/')
    
    if WorkTree == '':
        WorkTree = '/'
        
    ReplyCode = '226 sucessfully transfered"'+WorkTree+'"\r\n'
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
    
    Message = ( '227 Entering Passive Mode (' + Host +',' + str(p1) + ',' +str(p2) + ')\r\n' )
    connection.send(Message.encode("UTF-8"))
    
    ReplyCode = ('150 File status okay; about to open data connection.\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
    
    DataConnection, DataAddress = FileTransferSocket.accept()
    

    
    return DataConnection, DataAddress

##########################################################
######################This works 100%####################
def Store(Command,DataConnection,MarkerPosition=0):
    
    FileName = formatCommands(Command)    
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
        WorkTree = str(os.getcwd())
        WorkTree = WorkTree.replace(str(UsersDir),'')
        WorkTree = WorkTree.replace('\\','/')
        WorkTree = WorkTree +'/'+ FileName
        ReplyCode = ('226 Successfully transferred "'+WorkTree+'" \r\n')
        connection.send(ReplyCode.encode('UTF-8'))

    return

##########################################################
######################This works 100%####################
def retrieve(Command,DataConnection):
    
    FileName = formatCommands(Command)
    
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
            receiveCompressionMode(IncommingData,File)
        
        if ModeList[2] == True:
            
            IncommingData = recv_timeout(DataConnection)
            receiveBlockMode(File,IncommingData,0)
           
        
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print (FileName + ' has finished downloading\n')
        print(FileName +' ( ' +str(len(IncommingData)/1000) +' kB ) was downloaded in ' +str(ElapsedTime) +' seconds')
        File.close()
        
        ReplyCode = ('226 sucessfully transfered "'+FileName+'"\r\n')
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
    
    ReplyCode = ('257 "'+WorkTree+'" is current directory\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
    
    return

##########################################################
######################This works 100%####################
######DO NOT USE FOR ANYHTING OTHER THAN TEXTFILES######
def receiveCompressionMode(IncommingData,File):
    
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

    
    ReplyCode = ('200 Command okay, new port is ' + str(Port) +' and new host is ' +Host +'\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
    
    ReplyCode = ('150 File status okay; about to open data connection.\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
     
     
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((Host,Port))
#    FileTransferSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    FileTransferSocket.bind((Host,Port))
#    FileTransferSocket.listen(5)
#    DataConnection, DataAddress = FileTransferSocket.accept()
    
   
    
    return FileTransferSocket

#################Needs Testing#####################
###################################################
###################################################

def RestartFileTransfer(MarkerPosition):
    
    receiveBlockMode(MarkerPosition)

    return


#################Needs Testing#####################
###################################################
###################################################

def sendBlockMode(File,FileTransferSocket,MarkerPosition=0): 
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

    while NumberOfBytes > 65536:
        
        end = start + 65536
        Block = ('000000001111111111111111' + string2bits(str(File[start:end])))

        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        FileTransferSocket.send(Block)

        Block = ('000100000000000000000110' + string2bits(Marker))

        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        FileTransferSocket.send(Block)
        
        NumberOfBytes = NumberOfBytes - 65536

        start += 65537
    
    if NumberOfBytes > 0 and NumberOfBytes < 65536:
        
        Block =('01000000' + Number2bits(NumberOfBytes,16) + string2bits(File[start:]))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
            
        FileTransferSocket.send(Block)
                    
    return 

#################Needs Testing#####################
###################################################
###################################################

def receiveBlockMode(File,IncommingData,MarkerPosition=0):

    #128 is EOR ----------> No point in this 
    #64 is EOF ----------> done
    #32 is errors -------> no point in this
    #16 marker ---------->done
    Data = IncommingData
    
    if TypeList[0] == True:
        Data.decode('UTF-8')

    if TypeList[1] == True:
        Data.decode('cp500')

    if MarkerPosition !=0:
        
        k = MarkerPosition
        Header = Data[k:k+24]
        
    else:
        Header = Data[0:24]
        k =0
    
    while 1:
        
        if Header[0:8] == '01000000':
            
            #then it is EOF
            Number = int(Header[8:25],2)       
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, len(Data), 8)))
            File.close()
            break
        
        if Header[0:8] == '00000000':
            
            #There are no EOR/EOF/Errors/Markers
            Number = int(Header[8:25],2)+1
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 24, 8)))
        
        if Header[0:8]== '00010000':
            
            #there are markers
            MarkerPosition = k 
            Number = int(Header[8:25],2)
             
        k += Number*8 + 24
        Header = Data[k : k + 24] 
        
    return MarkerPosition

def makeDataConnection(Command):
    
    if PortList[0] == True:
        DataConnection, DataAddress = passiveMode(Host)
        print('The current connection is to: '+ str(DataAddress))
        
    if PortList[1] == True:
        DataConnection = ChangePort(Command)
    
    
       
    return DataConnection


ControlSocket =socket.socket()
ControlSocket.bind((Host, port))
ControlSocket.listen(5)  
connection, address = ControlSocket.accept() 


Initiation = ('220 Service established, Welcome to the Silver Server!\r\n')
connection.send(Initiation.encode("UTF-8"))

print ("Connection request from address: " + str(address))

while 1:
    
    Command = connection.recv(4096).decode("UTF-8")

    if Command[0:4] == 'PORT':
        
        PortList[0] = False
        PortList[1] = True
        print('portlist' + str(PortList))
        DataConnection= makeDataConnection(Command)
        continue
    
    if Command[0:4] == 'PASV':
        
        PortList[0] = True
        PortList[1] = False
        print('portlist' + str(PortList))
        DataConnection = makeDataConnection(Command)
        continue
    
    if Command[0:4] == 'QUIT':
        quitService()
        break;
        
    if Command[0:4] == 'USER':
        UsersDir = Login(port,Host,Command)
        continue
        
    if Command[0:4] == 'LIST':

       getDirectoryList(Command,UsersDir,DataConnection)
       continue
   
    if Command[0:4] == 'RETR':
        Store(Command,DataConnection,MarkerPosition=0)
        continue
    
    if Command[0:4] == 'STOR':
        retrieve(Command,DataConnection)
        continue
  
    if Command[0:4] == 'NOOP':
    
        NoOperation(Command)
        continue
    
    if Command[0:4] == 'REST':
        
        MarkerPosition = 0 #defualt value
        RestartFileTransfer(MarkerPosition) 
        continue

    if Command[0:4] == 'HELP':
       
       SOS(Command)
       continue
   
    if Command[0:3] == 'MKD':
        makeDirectory(Command)
        continue
    
    if Command[0:3] == 'RMD':
        removeDirectory(Command)
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
      response = ('500 Syntax command unrecognized\r\n')
      connection.send(response.encode("UTF-8")) 
    
    
connection.close()
    