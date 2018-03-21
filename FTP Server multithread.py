# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:31:42 2018

@author: Arlo Eardley
"""
import socket
import os
import time
import threading

port = 5000
Host = '127.0.0.1'

#Type List In order ASCII, EDCBIC, IMAGE
TypeList = [True, False, False]

#Mode list in order of Stream, Compressed, Block
ModeList = [True, False, False]

#for using the passive mode or Port mode in that order
PortList = [True,False]


class FTPserverThread(threading.Thread):
    
    def __init__(self,address, ControlSocket,connection):
        
            threading.Thread.__init__(self)
            self.connection = connection
            self.address = address
            self.ControlSocket = ControlSocket
            self.port = port
            self.Host = Host
            self.Command = ''
            self.PortList = [True,False]
            self.ModeList = [True, False, False]
            self.TypeList = [True, False, False]
            #self.CommandsOneParam =['USER','PASS','RETR','STOR','MKD','RMD','DELE','HELP','LIST','TYPE','MODE','CWD', 'PORT']
            print ("Connection request from address: " + str(address))
            
    #def __getitem__(self, key):
     #   return self.CommandsOneParam[key]
            
    def run(self):
        self.Initiation()
        
        while 1:
            
            Command = self.connection.recv(4096).decode("UTF-8")
            
            if Command[0:4] == 'PORT':
                
                self.PortList[0] = False
                self.PortList[1] = True
                self.DataConnection= self.makeDataConnection(Command)
                continue
            
            if Command[0:4] == 'PASV':
                
                self.PortList[0] = True
                self.PortList[1] = False
                self.DataConnection =self.makeDataConnection(Command)
                continue
            
            if Command[0:4] == 'QUIT':
                self.quitService(address)
                break;
                
            if Command[0:4] == 'USER':
                self.UsersDir = self.Login(port,Host,Command)
                continue
                
            if Command[0:4] == 'LIST':
        
               self.getDirectoryList(Command,self.UsersDir,self.DataConnection)
               continue
           
            if Command[0:4] == 'RETR':
                self.Store(self,Command,self.DataConnection,self.UsersDir)
                continue
            
            if Command[0:4] == 'STOR':
                self.retrieve(Command,self.DataConnection)
                continue
          
            if Command[0:4] == 'NOOP':
            
                self.NoOperation()
                continue
            
            if Command[0:4] == 'REST':
                
                MarkerPosition = 0 #defualt value
                self.RestartFileTransfer(self,MarkerPosition) 
                continue
        
            if Command[0:4] == 'HELP':
               
               self.SOS(Command)
               continue
           
            if Command[0:3] == 'MKD':
                self.makeDirectory(Command,self.UsersDir)
                continue
            
            if Command[0:3] == 'RMD':
                self.removeDirectory(Command,self.UsersDir)
                continue
            
            if Command[0:3] == 'CWD':
                self.changeWorkingDir(Command)
                continue
            
            if Command[0:4] == 'CDUP':
                self.changeToParentDir(self.UsersDir)
                continue
            
            if Command[0:4] == 'DELE':
                self.deleteFile(Command,self.UsersDir)
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
                self.printWorkingDir(self)
                continue
                
            else:
              self.response = ('500 Syntax command unrecognized\r\n')
              self.connection.send(self.response.encode("UTF-8")) 
            
            
        self.connection.close()
            
    def Login(self,port,Host,Command):
        
        self.ReceivedUserName = self.formatCommands(Command) 
        FileDirectory = os.path.abspath(self.ReceivedUserName)
        
        while 1:
            
            self.UserAuthenticate = self.FolderChecker(FileDirectory)
            
            if self.UserAuthenticate == 0:
                self.connection.send('404 User name inccorect!\r\n')
                self.ReceivedUserName = self.connection.recv(4096).decode("UTF-8")
                self.ReceivedUserName = self.formatCommands(self.ReceivedUserName)
                
            if self.UserAuthenticate == 1:
                self.UsersFile = FileDirectory +'/credentials.txt'
                self.RealUsername, self.RealPassword = self.readFile(self.UsersFile)
                break
            
        while 1:
        
            if self.ReceivedUserName == self.RealUsername:
                self.connection.send('331 User name ok, require password\r\n')
                break
        
            else:
                self.connection.send('404 User name inccorect!\r\n')
                self.ReceivedUserName = self.connection.recv(4096).decode("UTF-8")
                self.ReceivedUserName = self.formatCommands(self.ReceivedUserName)
    
    
        self.ReceivedPassword = self.connection.recv(4096).decode("UTF-8")
        self.ReceivedPassword = self.formatCommands(self.ReceivedPassword)
     
        while 1:
        
            if self.ReceivedPassword == self.RealPassword:
            
                self.connection.send('230 User logged in, current working directory is / \r\n')
                break
        
            else:
                self.connection.send('404 Password inccorect\r\n')
                self.ReceivedPassword = self.connection.recv(4096).decode("UTF-8")
                self.ReceivedPassword = self.formatCommands(self.ReceivedPassword)

        return FileDirectory
    

    def FolderChecker(self,FileDirectory):
        
        Pathname = (str(FileDirectory))
        IsDirectory =  os.path.isdir(Pathname)
       
        if IsDirectory == True:
    
          return 1
      
        else:
            
          return 0
    
    def formatCommands(self,Command):
        
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
            #Format the message to sen to Server
                  
        return ParameterOne
    
    ###########################################################
    ######################This works 100%####################
    def readFile(self,filename):

        filehandle = open(filename)
        self.UserName = filehandle.readline().strip()
        self.Password = filehandle.readline().strip()
        filehandle.close()
    
        return self.UserName, self.Password
    
    ###########################################################
    ######################This works 100%####################
    def quitService(self,address):
        
        ReplyCode = '221 Thank you come again!\r\n'
        self.connection.send(ReplyCode.encode("UTF-8"))
        print('User ' + str(address)+' has disconnected ')
        
        return
    
    ###########################################################
    ######################This works 100%####################
    def SOS(self,Command):
        
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
    
    ###########################################################
    ######################This works 100%####################
        
    def makeDirectory(self,Command,UsersDir):
        
        Path = self.formatCommands(Command)
        FullPath = str(UsersDir) + '\\' + str(Path)
        
        if not os.path.exists(FullPath):
            
            os.makedirs(FullPath)
            ReplyCode = ('257 "' + Path + '" has been created \r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
            
        else:
            
            ReplyCode = ('550 Requested action not taken, ' + Path + ' already exists\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
    
        return 
    
    ###########################################################
    ######################This works 100%####################
        
    def changeWorkingDir(self,Command):
        
        Path = self.formatCommands(Command)
        RealPath = Path.replace('/','\\')
        
        try:
            if Path == '/':
                
                os.chdir(self.UsersDir)
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
    
    def removeDirectory(self,Command,UsersDir):
        
        Path = self.formatCommands(Command)
        FullPath = (str(UsersDir) + '\\'+ str(Path))
    
        try:
            os.rmdir(FullPath)
            ReplyCode = ('250 Requested file action okay' + Path  + ' has been removed \r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
        
        except OSError:
            
            ReplyCode = ('550 Requested action not taken, ' + Path + ' is not empty\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
            
        return
    
    ###########################################################
    ######################This works 100%####################
        
    def changeToParentDir(self,UsersDir):
        
        os.chdir(UsersDir)
        print(os.getcwd())
        
        ReplyCode = ('200 Working directory changed to / \r\n' )
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        return 
    
    ###########################################################
    ######################This works 100%####################
        
    def deleteFile(self,Command,UsersDir):
        
        FileName = self.formatCommands(Command)
        Path = UsersDir + '\\' + FileName

        try:
            
            os.remove(Path)
            ReplyCode = ('250 Requested file action okay , ' + FileName+ ' has been deleted.\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
            
        except OSError:
            
            ReplyCode = ('450 Requested file action not taken, ' + FileName + ' is not a file\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
        
        
        return
    
    ###########################################################
    ######################This works 100%####################
    def changeType(self,Command,TypeList):
        
        ParameterOne = self.formatCommands(Command)
    
        if ParameterOne == 'A':
            
            ReplyCode = ('200 Command okay, the type has been set to ASCII for the session\r\n')
            
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
            ReplyCode = ('500 TYPE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
            
      
        self.connection.send(ReplyCode.encode('UTF-8'))
    
    
        return
    
    ###########################################################
    ######################This works 100%####################
    def changeMode(self,Command,ModeList):
        
        ParameterOne = self.formatCommands(Command)
       
        if ParameterOne == 'S':
            
            ReplyCode = ('200 Command okay, the mode has been set to Stream for the session\r\n')
            
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
            
            ReplyCode = ('500 MODE ' + ParameterOne + ' is unrecognized or not supported.\r\n')
            
            
        self.connection.send(ReplyCode.encode('UTF-8'))
    
        return
    
    ##########################################################
    ######################This works 100%####################
        
    def NoOperation(self):
        
        Response = "200 OK\r\n"
        self.connection.send(Response.encode("UTF-8")) 
        print('Performed no operation -_- ...')
        
        return
    
    ##########################################################
    ######################This works 100%####################
    def getDirectoryList(self,Command,UsersDir,DataConnection):
        
    
        Pathname = self.formatCommands(Command)
    
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
              
        self.DataConnection.send(FileList.encode('UTF-8'))
        
        WorkTree = str(UsersDir)
        WorkTree = WorkTree.replace(str(UsersDir),'')
        WorkTree = WorkTree.replace('\\','/')
        
        if WorkTree == '':
            WorkTree = '/'
            
        ReplyCode = '226 sucessfully transfered"'+WorkTree+'"\r\n'
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        self.DataConnection.shutdown(socket.SHUT_RDWR)
        self.DataConnection.close()
        
        return
    
    ##########################################################
    ######################This works 100%####################
    def passiveMode(self,Host):
        
        self.FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.FileTransferSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.FileTransferSocket.bind(('0.0.0.0', 0))
        self.FileTransferSocket.listen(5)
        self.DataPort = self.FileTransferSocket.getsockname()[1]
            
        self.p2 = self.DataPort % 256
        self.p1 = (self.DataPort -self.p2)/256
    
        self.Host = self.Host.replace('.',',')
        
        Message = ( '227 Entering Passive Mode (' + self.Host +',' + str(self.p1) + ',' +str(self.p2) + ')\r\n' )
        self.connection.send(Message.encode("UTF-8"))
        
        ReplyCode = ('150 File status okay; about to open data connection.\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        self.DataConnection, self.DataAddress = self.FileTransferSocket.accept()
        
    
        
        return self.DataConnection, self.DataAddress
    
    ##########################################################
    ######################This works 100%####################
    def Store(self,Command,DataConnection,UsersDir,MarkerPosition=0):
        
        FileName = self.formatCommands(Command) 
        print('filename in store')
        print(FileName)
        FileName = UsersDir + '\\' + FileName
        
        self.StartTimer = time.time()
    
        with open(FileName,'rb') as File:
        
            print(str(FileName) + ' has been opened...')
            
            if self.ModeList[0] == True:
                self.OutgoingData = File.read(8192)
                 
                while (self.OutgoingData):
                    
                    if self.TypeList[0] == True:
                        self.OutgoingData.encode('UTF-8')
        
                    if self.TypeList[1] == True:
                        self.OutgoingData.encode('cp500')
                    
                    self.DataConnection.send(self.OutgoingData)
                    self.OutgoingData = File.read(8192)
                    
            if self.ModeList[1]== True:
                
                self.sendCompressionMode(self.DataConnection,File)
            
            if ModeList[2] == True:
                
                self.sendBlockMode(File,self.DataConnection,MarkerPosition)
                
                
            self.StopTimer = time.time()
            self.ElapsedTime = self.StopTimer - self.StartTimer
            print(str(FileName) + ' has been sent to the client in '+ str(self.ElapsedTime) +' seconds')
            File.close()
            WorkTree = str(os.getcwd())
            WorkTree = WorkTree.replace(str(self.UsersDir),'')
            WorkTree = WorkTree.replace('\\','/')
            WorkTree = WorkTree +'/'+ FileName
            ReplyCode = ('226 Successfully transferred "'+WorkTree+'" \r\n')
            connection.send(ReplyCode.encode('UTF-8'))
    
        return
    
    ##########################################################
    ######################This works 100%####################
    def retrieve(self,Command,DataConnection):
        
        self.FileName = self.formatCommands(Command)
        
        self.StartTimer = time.time()
        
        print(self.FileName)
        print(os.getcwd())
    
        with open(self.FileName, 'wb') as self.File:
            
            if self.ModeList[0] == True:
                print(str(self.FileName) + ' has been opened...')
                
                IncommingData = self.recv_timeout(self.DataConnection)
                
                if self.TypeList[0] == True:
                    IncommingData.decode('UTF-8')
                    self.File.write(IncommingData)
                    
                if self.TypeList[1] == True:
                    IncommingData.decode('cp500')
                    self.File.write(IncommingData)
                    
                if self.TypeList[2] == True:
                    self.File.write(IncommingData)
                    
            if self.ModeList[1]== True:
                
                IncommingData = self.recv_timeout(self.DataConnection)
                self.receiveCompressionMode(IncommingData,self.File)
            
            if self.ModeList[2] == True:
                
                IncommingData = self.recv_timeout(self.DataConnection)
                self.receiveBlockMode(self.File,IncommingData,0)
               
            
            self.StopTimer = time.time()
            self.ElapsedTime = self.StopTimer - self.StartTimer
            print (self.FileName + ' has finished downloading\n')
            print(self.FileName +' ( ' +str(len(IncommingData)/1000) +' kB ) was downloaded in ' +str(self.ElapsedTime) +' seconds')
            self.File.close()
            
            ReplyCode = ('226 sucessfully transfered "'+self.FileName+'"\r\n')
            self.connection.send(ReplyCode.encode('UTF-8'))
    
        
        return 
    
    def string2bits(s='', bitnumer=8):
        
        List = [bin(ord(x))[2:].zfill(bitnumer) for x in s]
        
        return ''.join(List)
    
    
    def Number2bits(Number, NoBits):
        
        Number = bin(Number)[2:]
        
        return str(Number).zfill(NoBits)
    
    ##########################################################
    ######################This works 100%####################
    def printWorkingDir(self,UsersDir):
        
        WorkTree = str(os.getcwd())
        WorkTree = WorkTree.replace(str(UsersDir),'')
        
        if WorkTree == '':
            WorkTree = '/'
            
        else:
            WorkTree = WorkTree.replace('\\','/')
        
        ReplyCode = ('257 "'+WorkTree+'" is current directory\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))
        
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
    def recv_timeout(self,DataConnection,timeout=2):
        #make socket non blocking
        self.DataConnection.setblocking(0)
         
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
                data = self.DataConnection.recv(8192)
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
    
    def ChangePort(self,Command):
        
        Newport = self.formatCommands(Command)
        Newport = Newport.split(",")
        Host = ''
        
        for i in range(0,4):
            
            Host+= str(Newport[i])
            if i != 3:
                Host += "."
                
        self.Host = Host
        self.Port = int(str(hex(int(Newport[4]))[2:])  + str(hex(int(Newport[5]))[2:]),16)
    
        
        ReplyCode = ('200 Command okay, new port is ' + str(self.Port) +' and new host is ' +self.Host +'\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))
        
        ReplyCode = ('150 File status okay; about to open data connection.\r\n')
        self.connection.send(ReplyCode.encode('UTF-8'))
         
        self.FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.FileTransferSocket.connect((self.Host,self.Port))

        return self.FileTransferSocket
    
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
    
    def makeDataConnection(self,Command):
        
        if self.PortList[0] == True:
            self.DataConnection, self.DataAddress = self.passiveMode(Host)
            print('The current connection is to: '+ str(self.DataAddress))
            
        if self.PortList[1] == True:
           self.DataConnection = self.ChangePort(Command)
        
        return self.DataConnection
    
    def Initiation(self):
        
        ReplyCode= ('220 Service established, Welcome to the Silver Server!\r\n')
        self.connection.send(ReplyCode.encode("UTF-8"))
        
        return




ControlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ControlSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ControlSocket.bind(('', port))
 
print("The Silver Server is up and running!")
print("Awaiting client connection requests...")

while True:
    #serverSocket.listen(1)
    ControlSocket.listen(1)
    connection, address = ControlSocket.accept()
    newthread = FTPserverThread(address, ControlSocket,connection)
    newthread.start()





    