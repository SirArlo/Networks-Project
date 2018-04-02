# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:31:42 2018

@author: Arlo Eardley 1108472 and Carel Ross 1106684
"""
import socket
import os
import time
import threading

port = 5000
Host = '127.0.0.1'

#create the class for the FTP server
class FTPserverThread(threading.Thread):
    
    def __init__(self,address, ControlSocket,connection):
        #Initialising some variables
            threading.Thread.__init__(self)
            self.connection = connection
            self.address = address
            self.ControlSocket = ControlSocket
            self.port = port
            self.Host = Host
            self.Command = ''
            self.PortList = [True,False] #for using the passive mode or Port mode in that order
            self.ModeList = [True, False, False] #Mode list in order of Stream, Compressed, Block
            self.TypeList = [True, False, False]  #Type List In order ASCII, EDCBIC, IMAGE
            self.CurrentWorkDir = ''
            
            print ("Connection request from address: " + str(address))

    #This is the main loop that control the FTP server and calls the required functions based on the command received

    def run(self):
        self.Initiation()
        
        while 1:
            
            #Receive the request from the user
            Command = self.connection.recv(4096).decode("UTF-8")
            
            if Command[0:4] == 'PORT':
                
                #change the type of port to be used (PORT mode)
                self.PortList[0] = False
                self.PortList[1] = True
                self.DataConnection= self.makeDataConnection(Command)
                continue
            
            if Command[0:4] == 'PASV':
                 #change the type of port to be used (PASV mode)
                self.PortList[0] = True
                self.PortList[1] = False
                self.DataConnection =self.makeDataConnection(Command)
                continue
            
            if Command[0:4] == 'QUIT':
                self.quitService(address)
                break;
                
            if Command[0:4] == 'USER':
                self.UsersDir = self.Login(port,Host,Command)
                self.CurrentWorkDir = self.UsersDir
                print(self.CurrentWorkDir)
                continue
                
            if Command[0:4] == 'LIST':
        
               self.getDirectoryList(Command,self.UsersDir,self.DataConnection)
               continue
           
            if Command[0:4] == 'RETR':
                self.Store(Command,self.DataConnection,self.UsersDir)
                continue
            
            if Command[0:4] == 'STOR':
                self.retrieve(Command,self.DataConnection,self.UsersDir)
                continue
          
            if Command[0:4] == 'NOOP':
            
                self.NoOperation()
                continue
                    
            if Command[0:4] == 'HELP':
               
               self.SOS(Command)
               continue
           
            if Command[0:3] == 'MKD':
                self.makeDirectory(Command,self.CurrentWorkDir)
                continue
            
            if Command[0:3] == 'RMD':
                self.removeDirectory(Command,self.CurrentWorkDir)
                continue
            
            if Command[0:3] == 'CWD':
                self.changeWorkingDir(Command,self.CurrentWorkDir)
                continue
            
            if Command[0:4] == 'CDUP':
                self.changeToParentDir(self.CurrentWorkDir)
                continue
            
            if Command[0:4] == 'DELE':
                self.deleteFile(Command,self.CurrentWorkDir)
                continue
            
            if Command[0:4] =='TYPE':
                print(self.TypeList)
                self.changeType(Command,self.TypeList)
                print(self.TypeList)
                continue
            
            if Command[0:4] == 'MODE':
                print(self.ModeList)
                self.changeMode(Command,self.ModeList)
                print(self.ModeList)
                continue
                                                 
            if Command[0:3] == 'PWD':
                self.printWorkingDir(self.CurrentWorkDir)
                continue
                
            else:
            
              #this is for the case where the command has not been implemented
              self.response = ('500 Syntax error, command unrecognized\r\n')
              self.connection.send(self.response.encode("UTF-8")) 
            
         #close the control sonnection per user when they disconnect   
        self.connection.close()
            
    def Login(self,port,Host,Command):
         #Wrttien by Arlo Eardley 1108472
         #The login function processes the user and password commands, there is no anynonymous login
         #Users have to have username and password to use the server
           
        self.ReceivedUserName = self.formatCommands(Command) 
        FileDirectory = os.path.abspath(self.ReceivedUserName)
        
        while 1:
            
            self.UserAuthenticate = self.FolderChecker(FileDirectory) #Find the directory of the servers python file
            
            if self.UserAuthenticate == 0: #if user folder does not exist
                self.connection.send('530 user-name incorrect!\r\n')
                self.ReceivedUserName = self.connection.recv(4096).decode("UTF-8")
                self.ReceivedUserName = self.formatCommands(self.ReceivedUserName)
                
            if self.UserAuthenticate == 1:
                #user login details are stored in a file called credentials.txt
                self.UsersFile = FileDirectory +'/credentials.txt'
                #go and retrieve the user details from the file credentials.txt
                self.RealUsername, self.RealPassword = self.readFile(self.UsersFile)
                break
            
        while 1:
        
            if self.ReceivedUserName == self.RealUsername:
                #checks that the username matches the one inside the file credentials.txt
                self.connection.send('331 user-name ok, require password\r\n')
                break
        
            else:
                #otherwise the details are incorrect
                self.connection.send('530 user-name incorrect!\r\n')
                self.ReceivedUserName = self.connection.recv(4096).decode("UTF-8")
                self.ReceivedUserName = self.formatCommands(self.ReceivedUserName)
    
        #now the server can receive the password
        self.ReceivedPassword = self.connection.recv(4096).decode("UTF-8")
        self.ReceivedPassword = self.formatCommands(self.ReceivedPassword)
     
        while 1:
        
            if self.ReceivedPassword == self.RealPassword:
                #does the password received match that in the credentials.txt?
                self.connection.send('230 user logged in, current working directory is / \r\n')
                break
        
            else:
                #if not request the password again
                self.connection.send('530 Password inccorect\r\n')
                self.ReceivedPassword = self.connection.recv(4096).decode("UTF-8")
                self.ReceivedPassword = self.formatCommands(self.ReceivedPassword)

        return FileDirectory   #change the directory to the Users directory to keep files sepreate from other users
    

    def FolderChecker(self,FileDirectory):
            #This function takes in the username and find the folder named after the user
            #Checks if the user is valid and has login details

        Pathname = (str(FileDirectory))
        IsDirectory =  os.path.isdir(Pathname)
       
        if IsDirectory == True:
    
          return 1
      
        else:
            
          return 0
    
    def formatCommands(self,Command):
        #This function formats the commands and removes the parameters from the commands
        CommandsOneParam = ['USER','PASS','RETR','STOR','MKD','RMD','DELE','HELP','LIST','TYPE','MODE','CWD', 'PORT']
        ParameterOne = ''
     
        #Relies on the GUI entering a space after the command
        if str(Command)[0:4] in CommandsOneParam:
            
            #Obtain parameter by including whitespace in the removal
            
            ParameterOne = Command[Command.find(' ') + 1 :]  
            ParameterOne = ParameterOne.replace('\r\n','')
    
        #Special case for three char commands
        if str(Command)[0:3] in CommandsOneParam:
            
            #Obtain parameter by including whitespace in the removal
            ParameterOne = Command[Command.find(' ') + 1 :]
            ParameterOne = ParameterOne.replace('\r\n','')
            #Format the message to send to Server
                  
        return ParameterOne

    def readFile(self,filename):
        #This function reads the contents of credentials.txt and returns
        #the username and password inside the file

        filehandle = open(filename)
        self.UserName = filehandle.readline().strip()
        self.Password = filehandle.readline().strip()
        filehandle.close()
    
        return self.UserName, self.Password

    def quitService(self,address):
        #Wrttien by Arlo Eardley 1108472
        #This function quits the server after sending the godbye message
        ReplyCode = '221 Thank you come again!\r\n'
        self.connection.send(ReplyCode.encode("UTF-8"))
        print('User ' + str(address)+' has disconnected ')
        
        return

    def SOS(self,Command):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #this function is the HELP command that finds textfiles in the servers file directory
        #reads the contents and sends them to the client over the control connection
        #The parameter can either be HELP or the command specified in the HELP operation 

        Parameter = self.formatCommands(Command)
        
        Parameter = Parameter.upper()
        Filename = str(Parameter) + '.txt'
        Filename = (str(os.path.realpath(__file__)).replace('FTP Server multithread.py','') + str(Filename))
    
        with open(Filename,'rb') as HelpFile:
        
            ReplySOS = HelpFile.read()
            self.connection.send(ReplySOS)
        
            ReplyCode = '214 Help OK\r\n'
            self.connection.send(ReplyCode)
            
        HelpFile.close()
            
    
        return
    
        
    def makeDirectory(self,Command,CurrentWorkDir):
        #written by Carel Ross 1106684
        # this function makes a directory for the client
        #and creates the directory from the current working directory   

        Path = self.formatCommands(Command)
        FullPath = self.CurrentWorkDir + '\\' + str(Path)
        
        if not os.path.exists(FullPath):
            #checks if the path exists already
            os.makedirs(FullPath)        
            ReplyCode = ('257 "' + Path + '" has been created \r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
            
        else:
            #if folder does exist then the directory needs a different name

            ReplyCode = ('550 Requested action not taken, ' + Path + ' already exists\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
    
        return 
           
    def changeWorkingDir(self,Command,CurrentWorkDir):
        #written by Carel Ross 1106684
        #This function changes the current worki9ng directory

        Path = self.formatCommands(Command)
        RealPath = Path.replace('/','\\')
        
        try:
            if Path == '/':
                #if the path sent was the parent directory the CWD is set to the
                #users main directory (USERSDIR)  

                self.CurrentWorkDir = self.UsersDir
                ReplyCode = ('250 CWD successful "/" is current directory\r\n' )
                self.connection.send(ReplyCode.encode('UTF-8'))
    
            else:
                #othersie append the path onto the CWD and create the folder
                #worktree operations are for disclosure of information
                #providing the illusion that the user is in the root directory
                #even though they are in a computers documents directory

                WorkTree = CurrentWorkDir + RealPath
                self.CurrentWorkDir = WorkTree
                WorkTree = WorkTree.replace(str(self.UsersDir),'')
                print(WorkTree)
                WorkTree = WorkTree.replace('\\','/')
                print(WorkTree)
                ReplyCode = ('250 CWD successful."'+ WorkTree+'" is current directory\r\n' )
                self.connection.send(ReplyCode.encode('UTF-8'))
            
        except OSError:
            #if the user tries to change to a directory that does not exist throw an exception

            ReplyCode = '550 Requested action not taken, No such directory\r\n'
            self.connection.send(ReplyCode.encode('UTF-8'))
    
    
        return 
      
    def removeDirectory(self,Command,CurrentWorkDir):
        #Wrttien by Arlo Eardley 1108472
        #this function removes a directory by appending the selected path to the
        #users current working directory

        Path = self.formatCommands(Command)
        FullPath = (str(CurrentWorkDir) + '\\'+ str(Path))
    
        try:
            #try remove the directory is it is empty
            os.rmdir(FullPath)
            ReplyCode = ('250 Requested file action okay' + Path  + ' has been removed \r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
        
        except OSError:
            #clearly the directory was not empty and cannot be deleted
            ReplyCode = ('550 Requested action not taken, ' + Path + ' is not empty\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
            
        return
         
    def changeToParentDir(self,CurrentWorkDir):
        #written by Carel Ross 1106684
        #this function changes to the root/parent directory for the client
        #the users directory is a constant variable that never changes 

        self.CurrentWorkDir = self.UsersDir
        ReplyCode = ('200 Working directory changed to / \r\n' )
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        return 
        
    def deleteFile(self,Command,CurrentWorkDir):
        #Wrttien by Arlo Eardley 1108472
        # this function allows the client to delete a file in their directory
        #Filename is extracted from the command sent to the server

        FileName = self.formatCommands(Command)
        Path = CurrentWorkDir + '\\' + FileName

        try:
            #Try to remove the file if it is infact an existing file

            os.remove(Path)
            ReplyCode = ('250 Requested file action okay , ' + FileName+ ' has been deleted.\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
            
        except OSError:
            #clearly the file does not exist and therefore cannot be removed

            ReplyCode = ('450 Requested file action not taken, ' + FileName + ' is not a file\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
        
        return
    
    def changeType(self,Command,TypeList):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #This function changes the TYPE to ASCII EDCBIS or IMAGE and remains changed
        #for the duration fo the session although ASCII is the default TYPE

        ParameterOne = self.formatCommands(Command)
    
        if ParameterOne == 'A':
            
            ReplyCode = ('200 Command okay, the type has been set to ASCII for the session\r\n')

            #The for loops set all the varibles in the list to FALSE and then
            #Sets the requested type to true  

            for i in xrange(0, len(self.TypeList)):
                self.TypeList[i] = False
                
            self.TypeList[0] = True
            
        elif ParameterOne == 'E':
            
            ReplyCode = ('200 Command okay, the type has been set to EDCBIC for the session\r\n')
            
            for i in xrange(0, len(self.TypeList)):
                self.TypeList[i] = False
                
            self.TypeList[1] = True
             
        elif ParameterOne == 'I':
            
            ReplyCode = ('200 Command okay, the type has been set to Image/Binary for the session\r\n')
            
            for i in xrange(0, len(self.TypeList)):
                self.TypeList[i] = False
            
            self.TypeList[2] = True
            
        else:
            #otherwise if an unrecognised type is specified then the command cannot be implemented

            ReplyCode = ('500 TYPE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
            
      
        self.connection.send(ReplyCode.encode('UTF-8'))
    
    
        return

    def changeMode(self,Command,ModeList):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #This function is responsible for changing the MODES of sending
        #supported modes are STREAM, BLOCK and COMPRESSION  

        ParameterOne = self.formatCommands(Command)
       
        if ParameterOne == 'S':
            
            ReplyCode = ('200 Command okay, the mode has been set to Stream for the session\r\n')

            #The for loops set all the varibles in the list to FALSE and then
            #Sets the requested mode to true

            for i in xrange(0, len(self.ModeList)):
                self.ModeList[i] = False
                
            self.ModeList[0] = True
    
        elif ParameterOne == 'C':
            
            ReplyCode = ('200 Command okay, the mode has been set to Compression for the session\r\n')
            
            for i in xrange(0, len(self.ModeList)):
                self.ModeList[i] = False
                
            self.ModeList[1] = True
        
        elif ParameterOne == 'B':
            
            ReplyCode = ('200 Command okay, the mode has been set to Block for the session\r\n')
            
            for i in xrange(0, len(self.ModeList)):
                self.ModeList[i] = False
            
            self.ModeList[2] = True
            
        else:
            #Otherwise the requested mode has not been implemented and cannot be changed

            ReplyCode = ('500 MODE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
            
            
        self.connection.send(ReplyCode.encode('UTF-8'))
    
        return
        
    def NoOperation(self):
        #written by Carel Ross 1106684
        #this function replies to a NOOP command

        Response = "200 OK\r\n"
        self.connection.send(Response.encode("UTF-8")) 
        print('Performed no operation -_- ...')
        
        return
    
    def getDirectoryList(self,Command,UsersDir,DataConnection):
        #Wrttien by Arlo Eardley 1108472
        #This function performs the LIST command and sends the directory list 
        #over a previously established data connection using PASV

        Pathname = self.formatCommands(Command)
        
        print(Pathname)
        FileList = '\n'  

        #If there in not parameter then the LIST is just the CWD

        if Pathname == 'LIST':
            Pathname = self.CurrentWorkDir
            ListOfDirFiles = os.listdir(self.CurrentWorkDir)

        elif Pathname == '/':
            ListOfDirFiles = os.listdir(str(UsersDir))
            
        else:
            ListOfDirFiles = os.listdir(str(UsersDir) + str(Pathname))

        #remove the credentials.txt from the list so the user doesn't know the file containing their details
        #exists in their directory

        if 'credentials.txt' in ListOfDirFiles:
            ListOfDirFiles.remove('credentials.txt')  
            
        sorted(ListOfDirFiles)
        for i in ListOfDirFiles:
            FileList = FileList + str(i) +'\n'   
              
        self.DataConnection.send(FileList.encode('UTF-8'))

        #Format the directory listing for the user
        WorkTree = str(UsersDir) + str(Pathname)
        WorkTree = WorkTree.replace(str(UsersDir),'')
        WorkTree = WorkTree.replace('\\','/')
        
        if WorkTree == '':
            WorkTree = '/'
            
        ReplyCode = '226 successfully transfered"'+WorkTree+'"\r\n'
        self.connection.send(ReplyCode.encode('UTF-8'))
        self.DataConnection.shutdown(socket.SHUT_RDWR)
        self.DataConnection.close()
        
        return
    
    def passiveMode(self,Host):
        #Wrttien by Arlo Eardley 1108472
        #This function implements the PASV mode for data transfer
        #By setting up the datasocket and returning it to other functions to use
          
        self.FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.FileTransferSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #This allows the kernel to provide an open port to gurantee a connection on local host
        self.FileTransferSocket.bind(('0.0.0.0', 0))
        self.FileTransferSocket.listen(5)
        self.DataPort = self.FileTransferSocket.getsockname()[1]

        #Format the port and host to conform to FTP response message        
        self.p2 = self.DataPort % 256
        self.p1 = (self.DataPort -self.p2)/256
    
        self.Host = self.Host.replace('.',',')
        
        Message = ( '227 Entering Passive Mode (' + self.Host +',' + str(self.p1) + ',' +str(self.p2) + ')\r\n' )
        self.connection.send(Message.encode("UTF-8"))
        
        ReplyCode = ('150 File status okay; about to open data connection.\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        self.DataConnection, self.DataAddress = self.FileTransferSocket.accept()
         
        return self.DataConnection, self.DataAddress
    
    def Store(self,Command,DataConnection,UsersDir,MarkerPosition=0):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #This function implements the RETR command from the client (server storing data on client side)
           
        Document = self.formatCommands(Command) 
        FileName = self.CurrentWorkDir + '\\' +str(Document)
        
        self.StartTimer = time.time()
    
        with open(FileName,'rb') as File:
        
            print(str(FileName) + ' has been opened...')

            #Perform checks for modes and types currently being used
            if self.ModeList[0] == True:
                OutgoingData = File.read(8192)
                 
                while (OutgoingData):
                    
                    if self.TypeList[0] == True:
                        OutgoingData.encode('UTF-8') #This is ASCII
        
                    if self.TypeList[1] == True:
                        OutgoingData.encode('cp500') #This is EDCBIC encoding
                    
                    self.DataConnection.send(OutgoingData) #This is IMAGE
                    OutgoingData = File.read(8192)
                    
            if self.ModeList[1]== True:
                
                print('Sending ' + str(FileName) + ' in compression mode.')
                self.sendCompressionMode(self.DataConnection,File) #send in compression mode

            if self.ModeList[2] == True:
                
                print('Sending ' + str(FileName) + ' in block mode.')
                self.sendBlockMode(File,self.DataConnection,MarkerPosition) #send in block mode

                
            self.StopTimer = time.time()
            self.ElapsedTime = self.StopTimer - self.StartTimer
            print(str(Document) + ' has been sent to the client in '+ str(self.ElapsedTime) +' seconds')
            File.close()
            ReplyCode = ('226 successfully transfered"'+Document+'" \r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
            self.DataConnection.close()
            
        return
    
    def retrieve(self,Command,DataConnection,UsersDir):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #This implements the STOR command from the user (Server retrieving data from client)   

        Document = self.formatCommands(Command)
        FileName = self.CurrentWorkDir + '\\' +str(Document)
        self.StartTimer = time.time()
        
        with open(FileName, 'wb') as File:
            
            if self.ModeList[0] == True:
                print(str(FileName) + ' has been opened...')
                
                IncommingData = self.CatchAllData(self.DataConnection)

                #perform check for modes and types currently being used
                if self.TypeList[0] == True:
                    IncommingData.decode('UTF-8') #This is ASCII
                    File.write(IncommingData)
                    
                if self.TypeList[1] == True:
                    IncommingData.decode('cp500') #This is EDCBIC
                    File.write(IncommingData)
                    
                if self.TypeList[2] == True:
                    File.write(IncommingData) #This is IMAGE
                    
            if self.ModeList[1]== True:
                
                IncommingData = self.CatchAllData(self.DataConnection)
                print('Receiving ' + str(FileName) + ' in compression mode.')
                self.receiveCompressionMode(IncommingData,File)   #receive in compression mode

            if self.ModeList[2] == True:
                
                IncommingData = self.CatchAllData(self.DataConnection)
                print('Receiving ' + str(FileName) + ' in block mode.')
                self.receiveBlockMode(File,IncommingData,0)  #receive in block mode
 
            
            self.StopTimer = time.time()
            self.ElapsedTime = self.StopTimer - self.StartTimer
            print (Document + ' has finished downloading\n')
            print(Document +' ( ' +str(len(IncommingData)/1000) +' kB ) was downloaded in ' +str(self.ElapsedTime) +' seconds')
            File.close()
            
            ReplyCode = ('226 successfully transfered"'+Document+'"\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))

        return 
    
    def string2bits(self,s='', bitnumer=8):
         #This function converts a string of data into 8 bit binary string
         #Used for block mode   

        List = [bin(ord(x))[2:].zfill(bitnumer) for x in s]
        
        return ''.join(List)
    
    
    def Number2bits(self,Number, NoBits):
        #This function converts a decimal number into binary string of the required number of bits 
        #Used in block mode

        Number = bin(Number)[2:]
        
        return str(Number).zfill(NoBits)
    
    def printWorkingDir(self,CurrentWorkDir):
        #written by Carel Ross 1106684
        #This function implements the PWD command
    
        #perform directory manipulation for user
        WorkTree = CurrentWorkDir
        WorkTree = WorkTree.replace(str(self.UsersDir),'')
        
        if WorkTree == '':
            WorkTree = '/'
            
        else:
            WorkTree = WorkTree.replace('\\','/')
        
        ReplyCode = ('257 "'+WorkTree+'" is current directory\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        return
    
    def receiveCompressionMode(self,IncommingData,File):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #This function allows the receiving of data in compression mode
    
        #Initalise some variables
        Binary = IncommingData

        if self.TypeList[0] == True:
            Binary.decode('UTF-8')

        if self.TypeList[1] == True:
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
                 
                 Block=chr(int(Binary[k+9:k+16],2))

                #Write sequence to the file
                 File.write(Block)                 
                 
                 i += 1
             Number = 1

            #check if the header is of a block of non compressed data
            if Header[0] == '0':
             
             Number = int(Header[1:],2)  #find the number of non-repeated characters

             Block = ''.join(chr(int(Binary[i:i+8], 2)) for i in range(k+8, k + Number*8 + 1, 8))

             #Write sequence to the file
             File.write(Block)

             #Check if the block contains compressed space characters
            if Header[0] == '1' and Header[1] == '1':
                
                Number = int(Header[2:],2) # find the number of repeated spaces
                i =0
                while i<Number:
                    
                    Block = chr(int(Binary[k+9:k+16],2))
                                       
                    File.write(Block)
                    
                    i += 1
                Number = 0
                
            Header = Binary[k+Number*8 +8 : k+Number*8 + 16] #Find next header based on length of previous data
            k += Number*8 + 8
            
            if k == LengthOfDAta:
                break
                
        return
    
    def sendCompressionMode(self,DataConnection,File):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #This function implements the sending of data in compression mode  
         
        File = File.read() #Read all contents of file

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

                     Block  = ('01111111' + self.string2bits(DataToCompress[start:start + 127],8))

                     #Perform TYPE checks

                     if self.TypeList[0] == True:
                         Block.encode('UTF-8')
    
                     if self.TypeList[1] == True:
                        Block.encode('cp500')
                        
                     self.DataConnection.send(Block)
                     
                     start = start + 127
                     counter = counter - 127
                     
                    if counter > 0 and counter < 127:

                        #Format a block of unique characters less than 127 in length

                        Block = ('0' + self.Number2bits(counter,7) + self.string2bits(DataToCompress[start:start + counter],8))            
                        
                        if self.TypeList[0] == True:
                            Block.encode('UTF-8')
    
                        if self.TypeList[1] == True:
                            Block.encode('cp500')
                        
                        self.DataConnection.send(Block)

                #Check for where in the map there are repated sequences
                if Map[i] > 1:
     
                    NumberBlocks = Map[i] #find out how many there are 
                    
                    while NumberBlocks >= 63:

                        #Send repeated charcaters in block of up to 63 in length
                        Block = ('10111111' + str(self.string2bits(DataToCompress[i],8)))
                        
                        if self.TypeList[0] == True:
                            Block.encode('UTF-8')
    
                        if self.TypeList[1] == True:
                            Block.encode('cp500')
                        
                        self.DataConnection.send(Block)
                        NumberBlocks = NumberBlocks - 63

                    #If there are left over for the repeating sequences format them with their number of occurance
                    if NumberBlocks > 0 and NumberBlocks < 63:
                        
                        Block = ('10' + self.Number2bits(NumberBlocks,6) + str(self.string2bits(DataToCompress[i],8)))
                        
                        if self.TypeList[0] == True:
                            Block.encode('UTF-8')
    
                        if self.TypeList[1] == True:
                            Block.encode('cp500')
                        
                        self.DataConnection.send(Block)
    
                counter = 0  
                
            i +=1
            
     ##############end of while loop##################

        #Perform the operations above to the end of the file when there is unaccounted for data
        if counter > 0 :
               
            start = i -counter
            while counter >= 127:
    
             Block = ('01111111' + self.string2bits(DataToCompress[start:start + 127],8)) 
    
             if self.TypeList[0] == True:
                 Block.encode('UTF-8')
    
             if self.TypeList[1] == True:
                Block.encode('cp500')
                        
             self.DataConnection.send(Block)
             
             start = start + 127
             counter = counter - 127
             
            if counter > 0 and counter < 127:
    
                Block = ('0' + self.Number2bits(counter,7) + self.string2bits(DataToCompress[start:start + counter],8))
    
                if self.TypeList[0] == True:
                    Block.encode('UTF-8')
    
                if self.TypeList[1] == True:
                    Block.encode('cp500')
                        
                self.DataConnection.send(Block)
                
        return
    
    
    def CatchAllData(self,DataConnection,timeout=2):
        #This fucntion allows for the socket to receive all incomming data with no data loss
        
        #make socket non blocking
        self.DataConnection.setblocking(0)
        TotalData=[];
        Data='';
        begin = time.time()
        
        while 1:
            #if you got some data, then break after timeout
            if TotalData and time.time()-begin > timeout:
                break
             
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break
             
            #recv something
            try:
                Data = self.DataConnection.recv(8192)
                if Data:
                    TotalData.append(Data)
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
         
        #join all parts to make final string
        return ''.join(TotalData)
    
    def ChangePort(self,Command):
        #written by Carel Ross 1106684
        #This function performs the PORT command when the user
        #specifies a host and port to use for data transfer

        Newport = self.formatCommands(Command)
        Newport = Newport.split(",")
        Host = ''

        #Reconstruct the host into x.x.x.x rather than x,x,x,x
        for i in range(0,4):
            
            Host+= str(Newport[i])
            if i != 3:
                Host += "."
                
        self.Host = Host

        #re-format the port into single decimal number rather than two seperate decimal numbers
        self.Port = int(str(hex(int(Newport[4]))[2:])  + str(hex(int(Newport[5]))[2:]),16)
    
        
        ReplyCode = ('200 Command okay, new port is ' + str(self.Port) +' and new host is ' +self.Host +'\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        ReplyCode = ('150 File status okay; about to open data connection.\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))

        #send an inbound TCP request to the client on the specified Port and Host
        self.FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.FileTransferSocket.connect((self.Host,self.Port))

        return self.FileTransferSocket
    
    
    def sendBlockMode(self,File,FileTransferSocket,MarkerPosition=0): 
        #Wrttien by Arlo Eardley 1108472
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
            Block = ('000000001111111111111111' + self.string2bits(str(File[start:end])))

            #Peform the checks for the TYPES being used
            if self.TypeList[0] == True:
                Block.encode('UTF-8')
    
            if self.TypeList[1] == True:
                Block.encode('cp500')
                        
            FileTransferSocket.send(Block)

            #Insert a marker after everyblock of length 65536
            Block = ('000100000000000000000110' + self.string2bits(Marker))
    
            if self.TypeList[0] == True:
                Block.encode('UTF-8')
    
            if self.TypeList[1] == True:
                Block.encode('cp500')
                        
            FileTransferSocket.send(Block)
            
            NumberOfBytes = NumberOfBytes - 65536
    
            start += 65537

         #this must be the EOF data so package it accordingly
        if NumberOfBytes > 0 and NumberOfBytes < 65536:
            
            Block =('01000000' + self.Number2bits(NumberOfBytes,16) + self.string2bits(File[start:]))
            
            if self.TypeList[0] == True:
                Block.encode('UTF-8')
    
            if self.TypeList[1] == True:
                Block.encode('cp500')
                
            FileTransferSocket.send(Block)
                        
        return 
    
    def receiveBlockMode(self,File,IncommingData,MarkerPosition=0):
        #Wrttien by Arlo Eardley 1108472
        #written by Carel Ross 1106684
        #This function implements the receiving of information in block mode
        #The following headers have been used in this implementation
        #64(01000000) is EOF ----------> done
        #16(00010000) is marker ---------->done

        Data = IncommingData

        #perform the checks for the TYPES being used
        if self.TypeList[0] == True:
            Data.decode('UTF-8')
    
        if self.TypeList[1] == True:
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
                
                #then it is EOF
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
    
    def makeDataConnection(self,Command):
        #This function creates the data connection
        #based on whether or not the PORT or PASV command has been chosen
        #it returns the socket object to the function that calls it

        #This is the PASV mode check
        if self.PortList[0] == True:
            self.DataConnection, self.DataAddress = self.passiveMode(Host)
            print('The current connection is to: '+ str(self.DataAddress))

        #this is the PORT mode check
        if self.PortList[1] == True:
           self.DataConnection = self.ChangePort(Command)
        
        return self.DataConnection
    
    def Initiation(self):
        #This function implements the initiation message to send to the new client

        ReplyCode= ('220 Service established, Welcome to the Silver Server!\r\n')
        self.connection.send(ReplyCode.encode("UTF-8"))
        
        return

#Create the initial TCP control connection 
ControlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ControlSocket.bind(('', port))
 
print("The Silver Server is up and running!")
print("Awaiting client connection requests...")

while True:
    
    #Listen for incomming connections and start the new threads for new clients
    ControlSocket.listen(1)
    connection, address = ControlSocket.accept()
    newthread = FTPserverThread(address, ControlSocket,connection)
    newthread.start()