# -*- coding: utf-8 -*-
#!/usr/bin/python*-
"""
Created on Sun Mar 04 15:06:43 2018

@author: Arlo Eardley 1108472 and Carel Ross 1106684
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

def Login(port,Host, Command):
    #written by Arlo Eardley 1108472
    #The login function processes the user and password commands, there is no anynonymous login
    #Users have to have username and password to use the server
    
    ReceivedUserName = formatCommands(Command) 
    ServerFileDirectory = os.path.dirname(os.path.realpath('__file__')) #Find the directory of the servers python file

    while 1:
        
        UserAuthenticate = FolderChecker(ServerFileDirectory,ReceivedUserName)
        
        if UserAuthenticate == 0: #if user folder does not exist
            connection.send('530 user-name incorrect!\r\n')
            ReceivedUserName = connection.recv(4096).decode("UTF-8")
            ReceivedUserName = formatCommands(ReceivedUserName)
            
        if UserAuthenticate == 1:
            #user login details are stored in a file called credentials.txt
            UsersFile = os.path.join(ServerFileDirectory, str(ReceivedUserName) +'\credentials.txt')
            #go and retrieve the user details from the file credentials.txt
            RealUsername, RealPassword = readFile(UsersFile)
            break
        
    while 1:
    
        if ReceivedUserName == RealUsername: 
            #checks that the username matches the one inside the file credentials.txt
            connection.send('331 user-name ok, require password\r\n')
            break
    
        else:
            #otherwise the details are incorrect
            connection.send('530 user-name incorrect!\r\n')
            ReceivedUserName = connection.recv(4096).decode("UTF-8")
            ReceivedUserName = formatCommands(ReceivedUserName)

    #now the server can receive the password
    ReceivedPassword = connection.recv(4096).decode("UTF-8")
    ReceivedPassword = formatCommands(ReceivedPassword)
 
    while 1:
    
        if ReceivedPassword == RealPassword:
            #does the password received match that in the credentials.txt?
            connection.send('230 user logged in, current working directory is / \r\n')
            break
    
        else:
            #if not request the password again
            connection.send('530 Password incorrect\r\n')
            ReceivedPassword = connection.recv(4096).decode("UTF-8")
            ReceivedPassword = formatCommands(ReceivedPassword)
            
    #change the directory to the Users directory to keep files sepreate from other users
    os.chdir((str(ServerFileDirectory) +'\\'+ str(ReceivedUserName)))

    return os.getcwd()

def FolderChecker(ServerFileDirectory,ReceivedUserName):
    #This function takes in the username and find the folder named after the user
    #Checks if the user is valid and has login details
    
    Pathname = (str(ServerFileDirectory) +'\\'+ str(ReceivedUserName))
    IsDirectory =  os.path.isdir(Pathname)
   
    if IsDirectory == True:

      return 1
  
    else:
        
      return 0

def formatCommands(Message):
    #This function formats the commands and removes the parameters from the commands
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
        #Format the message to send to Server
              
    return ParameterOne

def readFile(filename):
    #This function reads the contents of credentials.txt and returns
    #the username and password inside the file

    filehandle = open(filename)
    UserName = filehandle.readline().strip()
    Password = filehandle.readline().strip()
    filehandle.close()

    return UserName, Password

def quitService():
    #written by Arlo Eardley 1108472
    #This function quits the server after sending the godbye message
    ReplyCode = '221 Thank you come again!\r\n'
    connection.send(ReplyCode.encode("UTF-8"))
    print('User ' + str(address)+' has disconnected ')
    
    return

def SOS(Command):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #this function is the HELP command that finds textfiles in the servers file directory
    #reads the contents and sends them to the client over the control connection
    #The parameter can either be HELP or the command specified in the HELP operation
    
    Parameter = formatCommands(Command)
    
    Parameter = Parameter.upper()
    Filename = str(Parameter) + '.txt'
    Filename = (str(os.path.realpath(__file__)).replace('FTP Server.py','') + str(Filename))

    with open(Filename,'rb') as HelpFile:
    
        ReplySOS = HelpFile.read()
        connection.send(ReplySOS)
    
        ReplyCode = '214 Help OK\r\n'
        connection.send(ReplyCode)
    HelpFile.close()
        

    return
   
def makeDirectory(Command):
    #written by Carel Ross 1106684
    # this function makes a directory for the client
    #and creates the directory from the current working directory
    
    Path = formatCommands(Command)
    FullPath = str(os.getcwd()) + '\\' + str(Path)
    
    if not os.path.exists(FullPath):
        #checks if the path exists already
        
        os.makedirs(FullPath)
        #All worktree operations show the files the users have acces to and not the
        #full file path of the computer it is running on to prevent attacks
        
        WorkTree = str(os.getcwd())
        WorkTree = WorkTree.replace(str(UsersDir),'')
        print(WorkTree)
        WorkTree = WorkTree.replace('\\','/')
        print(WorkTree)
        
        ReplyCode = ('257 "' + WorkTree + Path + '" has been created \r\n')
        connection.send(ReplyCode.encode('UTF-8'))
        
    else:
        #if folder does exist then the directory needs a different name
        
        ReplyCode = ('550 Requested action not taken, ' + Path + ' already exists\r\n')
        connection.send(ReplyCode.encode('UTF-8'))

    return 
    
def changeWorkingDir(Command):
    #written by Carel Ross 1106684
    #This function changes the current worki9ng directory
    
    Path = formatCommands(Command)
    RealPath = Path.replace('/','\\')
    
    try:
        if Path == '/':
            #if the path sent was the parent directory the CWD is set to the
            #users main directory (USERSDIR)
            
            os.chdir(UsersDir)
            ReplyCode = ('250 CWD successful "/" is current directory\r\n' )
            connection.send(ReplyCode.encode('UTF-8'))

        else:
            #othersie append the path onto the CWD and create the folder
            
            os.chdir(str(os.getcwd()) + str(RealPath))
            #again worktree operations are for disclosure of information
            #providing the illusion that the user is in the root directory
            #even though they are in a computers documents directory
            
            WorkTree = str(os.getcwd())
            WorkTree = WorkTree.replace(str(UsersDir),'')
            WorkTree = WorkTree.replace('\\','/')
            ReplyCode = ('250 CWD successful."'+ WorkTree+'" is current directory\r\n' )
            connection.send(ReplyCode.encode('UTF-8'))
        
    except OSError:
        #if the user tries to change to a directory that does not exist throw an exception
        
        ReplyCode = '550 Requested action not taken, No such directory\r\n'
        connection.send(ReplyCode.encode('UTF-8'))


    return 

def removeDirectory(Command):
    #written by Arlo Eardley 1108472
    #this function removes a directory by appending the selected path to the
    #users current working directory
    
    Path = formatCommands(Command)
    FullPath = ( str(os.getcwd()) + '\\'+ str(Path))

    try:
        #try remove the directory is it is empty
        os.rmdir(FullPath)
        ReplyCode = ('250 Requested file action okay' + Path  + ' has been removed \r\n')
        connection.send(ReplyCode.encode('UTF-8'))
    
    except OSError:
        #clearly the directory was not empty and cannot be deleted
        ReplyCode = ('550 Requested action not taken, ' + Path + ' is not empty\r\n')
        connection.send(ReplyCode.encode('UTF-8'))
        
    return
   
def changeToParentDir():
    #written by Carel Ross 1106684
    #this function changes to the root/parent directory for the client
    #the users directory is a constant variable that never changes 
    
    os.chdir(UsersDir)

    ReplyCode = ('200 Working directory changed to / \r\n' )
    connection.send(ReplyCode.encode('UTF-8'))
    
    return 
    
def deleteFile(Command):
    #written by Arlo Eardley 1108472
    #this function allows the client to delete a file in their directory
    #Filename is extracted from the command sent to the server
    
    FileName = formatCommands(Command)
    
    try:
        #Try to remove the file if it is infact an existing file
        
        os.remove(FileName)
        ReplyCode = ('250 Requested file action okay , ' + FileName+ ' has been deleted.\r\n')
        connection.send(ReplyCode.encode('UTF-8'))
        
    except OSError:
        #clearly the file does not exist and therefore cannot be removed
        
        ReplyCode = ('450 Requested file action not taken, ' + FileName + ' is not a file\r\n')
        connection.send(ReplyCode.encode('UTF-8'))
    
    
    return

def changeType(Command,TypeList):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function changes the TYPE to ASCII EDCBIS or IMAGE and remains changed
    #for the duration fo the session although ASCII is the default TYPE
    
    ParameterOne = formatCommands(Command)

    if ParameterOne == 'A':
        
        ReplyCode = ('200 Command okay, the type has been set to ASCII for the session\r\n')
        
        #The for loops set all the varibles in the list to FALSE and then
        #Sets the requested type to true
        
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
        #otherwise if an unrecognised type is specified then the command cannot be implemented
        
        ReplyCode = ('500 TYPE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
        
  
    connection.send(ReplyCode.encode('UTF-8'))


    return

def changeMode(Command,ModeList):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function is responsible for changing the MODES of sending
    #supported modes are STREAM, BLOCK and COMPRESSION
    
    ParameterOne = formatCommands(Command)
   
    if ParameterOne == 'S':
        
        ReplyCode = ('200 Command okay, the mode has been set to Stream for the session\r\n')
        
        #The for loops set all the varibles in the list to FALSE and then
        #Sets the requested mode to true
        
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
        #Otherwise the requested mode has not been implemented and cannot be changed
        
        ReplyCode = ('500 MODE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
        
        
    connection.send(ReplyCode.encode('UTF-8'))

    return
    
def NoOperation(Command):
    #written by Carel Ross 1106684
    #this function replies to a NOOP command
    
    Response = "200 OK\r\n"
    connection.send(Response.encode("UTF-8")) 
    print('Performed no operation -_- ...')
    
    return

def getDirectoryList(Command,UsersDir,DataConnection):
    #written by Arlo Eardley 1108472
    #This function performs the LIST command and sends the directory list 
    #over a previously established data connection using PASV

    Pathname = formatCommands(Command)

    #If there in not parameter then the LIST is just the CWD
    if Pathname == 'LIST':
        Pathname = '\\'
        
    #Some formatting for information disclosure about computer directories
    if Pathname == '/':
        Pathname = ''

    FileList = '\n'  
    
    #Get a list of all the files in the CWD
    ListOfDirFiles = os.listdir(str(UsersDir) + str(Pathname))

    #remove the credentials.txt from the list so the user doesn't know the file containing their details
    #exists in their directory
    if 'credentials.txt' in ListOfDirFiles:
        ListOfDirFiles.remove('credentials.txt')  
        
    sorted(ListOfDirFiles)
    for i in ListOfDirFiles:
        FileList = FileList + str(i) +'\n'   
          
    DataConnection.send(FileList.encode('UTF-8'))
    
    #format the directory listing for the user
    WorkTree = str(os.getcwd())
    WorkTree = WorkTree.replace(str(UsersDir),'')
    WorkTree = WorkTree.replace('\\','/')
    
    if WorkTree == '':
        WorkTree = '/'
        
    ReplyCode = '226 successfully transfered"'+WorkTree+'"\r\n'
    connection.send(ReplyCode.encode('UTF-8'))
    
    DataConnection.shutdown(socket.SHUT_RDWR)
    DataConnection.close()
    
    return

def passiveMode(Host):
    #written by Arlo Eardley 1108472
    #This function implements the PASV mode for data transfer
    #By setting up the datasocket and returning it to other functions to use

    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #This allows the kernel to provide an open port to gurantee a connection on local host
    FileTransferSocket.bind(('0.0.0.0', 0))
    FileTransferSocket.listen(5)
    DataPort = FileTransferSocket.getsockname()[1]
        
    #Format the port and host to conform to FTP response message
    p2 = DataPort % 256
    p1 = (DataPort -p2)/256

    Host = Host.replace('.',',')
    
    Message = ( '227 Entering Passive Mode (' + Host +',' + str(p1) + ',' +str(p2) + ')\r\n' )
    connection.send(Message.encode("UTF-8"))
    
    ReplyCode = ('150 File status okay; about to open data connection.\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
    
    DataConnection, DataAddress = FileTransferSocket.accept()
      
    return DataConnection, DataAddress

def Store(Command,DataConnection,MarkerPosition=0):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function implements the RETR command from the client (server storing data on client side)
    FileName = formatCommands(Command)    
    StartTimer = time.time()

    with open(FileName,'rb') as File:
    
        print(str(FileName) + ' has been opened...')
        
        #Perform checks for modes and types currently being used
        
        if ModeList[0] == True:
            OutgoingData = File.read(8192)
             
            while (OutgoingData):
                
                if TypeList[0] == True:
                    OutgoingData.encode('UTF-8') #This is ASCII
    
                if TypeList[1] == True:
                    OutgoingData.encode('cp500') #This is EDCBIC encoding
                
                DataConnection.send(OutgoingData) #This is IMAGE
                OutgoingData = File.read(8192)
                
        if ModeList[1]== True:
            
            sendCompressionMode(DataConnection,File) #send in compression mode
        
        if ModeList[2] == True:
            
            sendBlockMode(File,DataConnection,MarkerPosition) #send in block mode
            
            
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print(str(FileName) + ' has been sent to the client in '+ str(ElapsedTime) +' seconds')
        File.close()
        #Worktree operations to send filepath to user including the file just downloaded
        WorkTree = str(os.getcwd())
        WorkTree = WorkTree.replace(str(UsersDir),'')
        WorkTree = WorkTree.replace('\\','/')
        WorkTree = WorkTree +'/'+ FileName
        ReplyCode = ('226 successfully transfered"'+WorkTree+'" \r\n')
        DataConnection.close()
        connection.send(ReplyCode.encode('UTF-8'))

    return

def retrieve(Command,DataConnection):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This implements the STOR command from the user (Server retrieving data from client)
    
    FileName = formatCommands(Command)
    StartTimer = time.time()
    
    with open(FileName, 'wb') as File:
        
        #perform check for modes and types currently being used
        
        if ModeList[0] == True:
            print(str(FileName) + ' has been opened...')
            
            IncommingData = CatchAllData(DataConnection)
            
            if TypeList[0] == True:
                IncommingData.decode('UTF-8') #This is ASCII
                File.write(IncommingData)
                
            if TypeList[1] == True:
                IncommingData.decode('cp500') #This is EDCBIC
                File.write(IncommingData)
                
            if TypeList[2] == True:
                File.write(IncommingData) #This is IMAGE
                
        if ModeList[1]== True:
            
            IncommingData = CatchAllData(DataConnection)
            receiveCompressionMode(IncommingData,File) #receive in compression mode
        
        if ModeList[2] == True:
            
            IncommingData = CatchAllData(DataConnection)
            receiveBlockMode(File,IncommingData,0) #receive in block mode
           
        
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print (FileName + ' has finished downloading\n')
        print(FileName +' ( ' +str(len(IncommingData)/1000) +' kB ) was downloaded in ' +str(ElapsedTime) +' seconds')
        File.close()
        
        ReplyCode = ('226 successfully transfered"'+FileName+'"\r\n')
        connection.send(ReplyCode.encode('UTF-8'))

    
    return 

def string2bits(s='', bitnumer=8):
    #This function converts a string of data into 8 bit binary string
    #Used for block mode
    
    List = [bin(ord(x))[2:].zfill(bitnumer) for x in s]
    
    return ''.join(List)


def Number2bits(Number, NoBits):
    #This function converts a decimal number into binary string of the required number of bits 
    #Used in block mode
    
    Number = bin(Number)[2:]
    
    return str(Number).zfill(NoBits)

def printWorkingDir():
    #written by Carel Ross 1106684
    #This function implements the PWD command
    
    #perform directory manipulation for user
    WorkTree = str(os.getcwd())
    WorkTree = WorkTree.replace(str(UsersDir),'')
    
    if WorkTree == '':
        WorkTree = '/'
        
    else:
        WorkTree = WorkTree.replace('\\','/')
    
    ReplyCode = ('257 "'+WorkTree+'" is current directory\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
    
    return

def receiveCompressionMode(IncommingData,File):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function allows the receiving of data in compression mode
    
    #Initalise some variables
    Binary = IncommingData
    
    if TypeList[0] == True:
        Binary.decode('UTF-8')

    if TypeList[1] == True:
        Binary.decode('cp500')
        
    LengthOfDAta = len(Binary)
    #set the first block header
    Header = Binary[0:8]
    Number = 0
    k =0
    
    while 1:
        
        # this check if the block contains a compressed repeated amount of characters
        if Header[0] == '1' and Header[1] == '0':

         Number = int(Header[2:],2) # find the number of repeated characters

         i =0

         while i < Number:
             
             Block = chr(int(Binary[k+9:k+16],2))
             
             File.write(Block)
             
             i += 1
         Number = 1
         
         #check if the header is of a block of non compressed data
        if Header[0] == '0':
         
         Number = int(Header[1:],2)# find the number of non-repeated characters
         
         Block = ''.join(chr(int(Binary[i:i+8], 2)) for i in range(k+8, k + Number*8 + 1, 8))

         File.write(Block)
        
         #Check if the block contains compressed space characters
        if Header[0] == '1' and Header[1] == '1':
            
            Number = int(Header[2:],2) # find the number of repeated spaces
            i =0
            while i<Number:
                
                Block = chr(int(Binary[k+9:k+16],2))

                #Write sequence to the file
                File.write(Block)
                
                i += 1
            Number = 0
            
        Header = Binary[k+Number*8 +8 : k+Number*8 + 16] #Find next header based on length of previous data
        k += Number*8 + 8
        
        if k == LengthOfDAta:
            break
            
    return

def sendCompressionMode(DataConnection,File):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function implements the sending of data in compression mode
    
    File = File.read()  #Read all contents of file
    
    #data to compress is a string of uniquie 
    #non repeating characters at the end of first while loop
    #And Map is a list of number corrsponding to the DataToCompress string
    #i.e AABCCD becomes
    #DataToCompress = ABCD
    #Map = [2,1,2,1]
    
    DataToCompress = ''
    l = len(File)
    Iter = 1
    i = 1
    Map = []
    
    while i < l:
        
        #Check if the previous charcater is the same as the current character
        if File[i] == File[i - 1]:
            
            Iter += 1
            
        else:
            #When the charcaters are not the same then append the charcater to a list 
            DataToCompress = DataToCompress + File[i - 1] 
            Map.append(Iter) #list of the character count
            Iter = 1
            
        i += 1
        
    DataToCompress = DataToCompress + File[i - 1]
    Map.append(Iter)


    counter = 0
    i = 0
    
    #Cycle through the compressed data and send it in blocks with correct headers
    while i <len(DataToCompress):
        
        #find the number of unique characters up to 127
        
        if Map[i] == 1:
            
            counter += 1
    
        else:
            
            if counter > 0 :
                       
                start = i -counter
                while counter >= 127:
                    
                #break up data and send it in block of the non-repeating sequences
                    
                 Block  = ('01111111' + string2bits(DataToCompress[start:start + 127],8))
                 
                 #Perform TYPE checks
                 
                 if TypeList[0] == True:
                     Block.encode('UTF-8')

                 if TypeList[1] == True:
                    Block.encode('cp500')
                    
                 DataConnection.send(Block)
                 
                 start = start + 127
                 counter = counter - 127
                 
                if counter > 0 and counter < 127:
                    
                    #Format a block of unique characters less than 127 in length
                    
                    Block = ('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8))            
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    DataConnection.send(Block)
            
            #Check for where in the map there are repated sequences
            if Map[i] > 1:
 
                NumberBlocks = Map[i] #find out how many there are 
                
                while NumberBlocks >= 63:
                    
                    #Send repeated charcaters in block of up to 63 in length
                    Block = ('10111111' + str(string2bits(DataToCompress[i],8)))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    DataConnection.send(Block)
                    NumberBlocks = NumberBlocks - 63
                
                #If there are left over for the repeating sequences format them with their number of occurance
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
 
 #Perform the operations above to the end of the file when there is unaccounted for data
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

def CatchAllData(socket,timeout=2):
    #make socket non blocking
    socket.setblocking(0)
    TotalData=[];
    Data='';
    begin=time.time()
    
    while 1:
        #if you got some data, then break after timeout
        if TotalData and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
        #recv something
        try:
            Data = socket.recv(8192)
            if Data:
                TotalData.append(Data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(TotalData)

def ChangePort(Command):
    #written by Carel Ross 1106684
    #This function performs the PORT command when the user
    #specifies a host and port to use for data transfer

    Newport = formatCommands(Command)
    Newport = Newport.split(",")
    Host = ''
    
    #Reconstruct the host into x.x.x.x rather than x,x,x,x
    for i in range(0,4):
        
        Host+= str(Newport[i])
        if i != 3:
            Host += "."
            
    #re-format the port into single decimal number rather than two seperate decimal numbers
    
    Port = int(str(hex(int(Newport[4]))[2:])  + str(hex(int(Newport[5]))[2:]),16)

    ReplyCode = ('200 Command okay, new port is ' + str(Port) +' and new host is ' +Host +'\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
    
    ReplyCode = ('150 File status okay; about to open data connection.\r\n')
    connection.send(ReplyCode.encode('UTF-8'))
     
    #send an inbound TCP request to the client on the specified Port and Host
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((Host,Port))

    return FileTransferSocket

def sendBlockMode(File,FileTransferSocket,MarkerPosition=0): 
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function implements the sending of information in block mode
    #The following headers have been used in this implementation
    #64(01000000) is EOF ----------> done
    #16(00010000) is marker ---------->done
    
    
    File = File.read()
    NumberOfBytes = len(File)
    Marker = 'rrrrrr' #set the markers to random string of charcaters
    
    #performs some checks related to the restart of the transfer i.e marker position
    if MarkerPosition != 0: 
        
        start = MarkerPosition
        
    else:
        
        start = 0
        
    #start to package the data into blocks of up to 65536 in size
    while NumberOfBytes > 65536:
        
        end = start + 65536
        #package blocks that arent markers of EOF
        Block = ('000000001111111111111111' + string2bits(str(File[start:end])))

        #Peform the checks for the TYPES being used
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        FileTransferSocket.send(Block)
        
        #Insert a marker after everyblock of length 65536
        Block = ('000100000000000000000110' + string2bits(Marker))

        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        FileTransferSocket.send(Block)
        
        NumberOfBytes = NumberOfBytes - 65536

        start += 65537
    
    #this must be the EOF data so package it accordingly
    if NumberOfBytes > 0 and NumberOfBytes < 65536:
        
        Block =('01000000' + Number2bits(NumberOfBytes,16) + string2bits(File[start:]))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
            
        FileTransferSocket.send(Block)
                    
    return 

def receiveBlockMode(File,IncommingData,MarkerPosition=0):
    #written by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function implements the receiving of information in block mode
    #The following headers have been used in this implementation
    #64(01000000) is EOF ----------> done
    #16(00010000) is marker ---------->done
    
    Data = IncommingData
    
    #perform the checks for the TYPES being used
    if TypeList[0] == True:
        Data.decode('UTF-8')

    if TypeList[1] == True:
        Data.decode('cp500')

    #check if the transfer has been restarted
    if MarkerPosition !=0:
        
        k = MarkerPosition
        Header = Data[k:k+24]
        
    else:
        Header = Data[0:24]
        k =0
    
    while 1:
        
         #This is the EOF header block 
        if Header[0:8] == '01000000':
            
           
            Number = int(Header[8:25],2) #extract the length of the data to follow
            
            #convert data from binary string to charcaters again and write to file
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, len(Data), 8)))
            File.close()
            break
        
        #There are no EOF/Markers
        if Header[0:8] == '00000000':
            
            
            Number = int(Header[8:25],2)+1 #extract the length of the data to follow
            
            #convert data from binary string to charcaters again and write to file
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 24, 8)))
        
        #This is the header for a marker block
        if Header[0:8]== '00010000':
            
            #Set marker position to current iteration of loop
            MarkerPosition = k 
            Number = int(Header[8:25],2)
             
        k += Number*8 + 24
        Header = Data[k : k + 24] #Find the next header in the bit stream
        
    return MarkerPosition

def makeDataConnection(Command):
    #This function creates the data connection
    #based on whether or not the PORT or PASV command has been chosen
    #it returns the socket object to the function that calls it
    
    #This is the PASV mode check
    if PortList[0] == True:
        DataConnection, DataAddress = passiveMode(Host)
        print('The current connection is to: '+ str(DataAddress))
        
    #this is the PORT mode check
    if PortList[1] == True:
        DataConnection = ChangePort(Command)
     
    return DataConnection

#Create the initial TCP control connection 
    
ControlSocket =socket.socket()
ControlSocket.bind((Host, port))
ControlSocket.listen(5)  
connection, address = ControlSocket.accept() 

#Set and send the server welcome message

Initiation = ('220 Service established, Welcome to the Silver Server!\r\n')
connection.send(Initiation.encode("UTF-8"))

print ("Connection request from address: " + str(address))

while 1:
    
    #Receive command from client
    Command = connection.recv(4096).decode("UTF-8")

    #when the command mathches one of these conditions then perform the required actions
    
    if Command[0:4] == 'PORT':
        
        #Change the type of port to be used
        PortList[0] = False
        PortList[1] = True
        DataConnection= makeDataConnection(Command)
        continue
    
    if Command[0:4] == 'PASV':
        
        #Change the type of port to be used
        PortList[0] = True
        PortList[1] = False
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
        
      # if none of the commands match then it hasnt been implemented 
      response = ('500 Syntax, command unrecognized\r\n')
      connection.send(response.encode("UTF-8")) 
    
    
connection.close()
    