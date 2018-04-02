# -*- coding: utf-8 -*-
#!/usr/bin/python 
"""
Created on Thu Feb 22 17:03:26 2018
@author: Arlo Eardley 1108472 and Carel Ross 1106684
"""
import socket
import time
import os

port = 5000
Host = 'localhost'

#Type List In order ASCII, EDCBIC, IMAGE
TypeList = [True, False, False]

#Mode list in order of Stream, Compressed, Block
ModeList = [True, False, False]

#for using the passive mode or Port mode in that order
PortList = [True,False]

#Accept the intial control connection socket

ControlSocket = socket.socket()
ControlSocket.connect((Host,port))

def Login(port,Host): 
    #Wrttien by Arlo Eardley 1108472
    #this function allows for the user to input their login details
    #it is called first and thus does not allows the user to acess a
    #server without login info
    
    #Establish the connection hopefully receiving the 220 Service Ready
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Reply from server:\n' + str(Reply))
    
    ReplyCode = ''
    while 1:
        
        #accept user input for Username
        Username = raw_input('Enter username: ')
        Message,_ = formatCommands(Username)

        ControlSocket.send(Message.encode('UTF-8'))
        ReplyCode = ControlSocket.recv(4096).decode('UTF-8')
        print( 'Reply from server: \n' + str(ReplyCode))
        
        #if the reply code is good then break and move on to password
        if ReplyCode[0:3] == '331' or ReplyCode[0:3] =='230':
            break
        
    ReplyCode =''
    while 1:
        
        #Put in the user password
        Password = raw_input('Enter Password: ')
        Message,_ = formatCommands(Password)

        ControlSocket.send(Message.encode('UTF-8'))
        ReplyCode = ControlSocket.recv(4096).decode('UTF-8')
        print('Reply from server: \n' + str(ReplyCode))
        
        #If the password is accepted move on
        if ReplyCode[0:3] == '230':
            break

    return

def getList(Message,FileTransferSocket):
    #Wrttien by Arlo Eardley 1108472
    #this function implemets the LIST commandand 
    #receives the directory list from server
    #NB it must be preceeded by a PORT or PASV command
    
    Message,_ = formatCommands(Message)
      
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    
    print('Control connection: \n' + str(Reply))
    
    Reply = FileTransferSocket.recv(4096).decode('UTF-8')
    print('Data port reply:\n ' + str(Reply))
    
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection:\n ' + str(Reply))

    return

def NoOperation(Message):
    #written by Carel Ross 1106684
    #This function implements the NOOP command
    
    Message = Message +'\r\n'
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')

    if Reply[0:3] == '200':
        
        print(Reply)
        
    else:
        
        print(Reply)
    
    return

def passiveMode():
    #Wrttien by Arlo Eardley 1108472
    #This function implements the PASV command
    #the return is used in the makeDataConnection() function
    #to use the port and host to create the connection
    
    Message,_ = formatCommands('PASV')
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print( '\n' + str(Reply))
    
    #Format the reply from the server for the port and host to be made
    start = Reply.find('(')
    end = Reply.find(')')
    Reply = Reply[start+1:end]
    Reply = Reply.split(',')
    DataHost = str(Reply[0]) + '.'+ str(Reply[1]) +'.'+ str(Reply[2]) +'.'+ str(Reply[3])
    DataPort = (int(Reply[4])*256) + int(Reply[5])
    
    return DataHost,DataPort


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
   
def quitService(Message):
    #Wrttien by Arlo Eardley 1108472
    #This function handles the QUIT command
    #After response is received the main while loop down below is exited
    #and the control connection is terminated
    
    Message,_= formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

def getHelp(Message):
    #written by Carel Ross 1106684
    #Wrttien by Arlo Eardley 1108472
    #This function implements the HELP command
    
    Message,_ = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    
    Reply = ControlSocket.recv(8192).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    Reply = ControlSocket.recv(8192).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
        
    return

def changeType(Message,TypeList):
    #Wrttien by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function changes the TYPE to ASCII EDCBIS or IMAGE and remains changed
    #for the duration fo the session although ASCII is the default TYPE
    
    Message,ParameterOne = formatCommands(Message)

    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    #make sure the server has implemented these TYPES
    if Reply[0:3] == '200':
        
        if ParameterOne == 'A': #ASCII
            
            #The for loops set all the varibles in the list to FALSE and then
            #Sets the requested type to true
            for i in xrange(0, len(TypeList)):
                TypeList[i] = False
                
            TypeList[0] = True
            
        if ParameterOne == 'E':#EDCBIC
            
            for i in xrange(0, len(TypeList)):
                TypeList[i] = False
                
            TypeList[1] = True
             
        if ParameterOne == 'I':#IMAGE/Binary
        
            for i in xrange(0, len(TypeList)):
                TypeList[i] = False
            
            TypeList[2] = True

    return

def Retrieve(Message,TypeList,FileTransferSocket,MarkerPosition=0):
    #Wrttien by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function implements the RETR command for the client
    
    Message,Filename = formatCommands(Message)
     
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    StartTimer = time.time()

    with open(Filename, 'wb') as File:
        
        #Perform the checks for the MODES being used
        if ModeList[0] == True:
            print(str(Filename) + ' has been opened...')
            
            IncommingData = CatchAllData(FileTransferSocket)
            
            #Perform the checks for the TYPES being used
            if TypeList[0] == True:
                IncommingData.decode('UTF-8') #ASCII
                File.write(IncommingData)
                
            if TypeList[1] == True:
                IncommingData.decode('cp500') #EDCBIC
                File.write(IncommingData)
                
            if TypeList[2]== True:
                File.write(IncommingData) #IMAGE/Binary
                
        if ModeList[1]== True:
            
           IncommingData = CatchAllData(FileTransferSocket)
           receiveCompressionMode(FileTransferSocket,IncommingData,File) #Receive in compression mode
        
        if ModeList[2] == True:
            
            IncommingData = CatchAllData(FileTransferSocket)
            receiveBlockMode(File,FileTransferSocket,IncommingData,0) #Receive in block mode
           
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print (str(Filename) + ' has finished downloading\n')
        print(str(len(IncommingData)/1000) +' kB of data was downloaded in ' +str(ElapsedTime) +' seconds')
        File.close()
        FileTransferSocket.close()
            
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    
    return

def Store(Message,TypeList,FileTransferSocket,MarkerPosition=0):
    #written by Carel Ross 1106684
    #Wrttien by Arlo Eardley 1108472
     #This function implements the STOR command for the client
     
    Message,ParameterOne = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('\nControl connection reply: \n' + str(Reply))
    
    StartTimer = time.time()

    with open(ParameterOne,'rb') as File:
    
        print(str(ParameterOne) + ' has been opened...\n\n')
        
        #Perform the checks for the MODES being used
        
        if ModeList[0] == True:
            OutgoingData = File.read(8192)
             
            while (OutgoingData):
                
                #Perform the checks for the TYPES being used
                
                if TypeList[0] == True:
                    OutgoingData.encode('UTF-8') #ASCII
    
                if TypeList[1] == True:
                    OutgoingData.encode('cp500') #EDCBIC
                
                FileTransferSocket.send(OutgoingData) #IMAGE/Binary
                OutgoingData = File.read(8192)
                
        if ModeList[1]== True:
            
            sendCompressionMode(File,FileTransferSocket)
        
        if ModeList[2] == True:
            
            sendBlockMode(File,FileTransferSocket,MarkerPosition)
            
            
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print(str(ParameterOne) + ' ( ' + str(os.path.getsize(ParameterOne)/1000) +' kB ) has been uploaded to the server in '+ str(ElapsedTime) +' seconds\n\n')
        FileTransferSocket.close()
        File.close()
        
        Reply = ControlSocket.recv(4096).decode('UTF-8')
        print('Control connection reply: \n' + str(Reply))
    
    return

def changeMode(Message,ModeList):
    #Wrttien by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function is responsible for changing the MODES of sending
    #supported modes are STREAM, BLOCK and COMPRESSION
    
    Message, ParameterOne = formatCommands(Message)
   
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))

    #Provided the reply has been implemented
    if Reply[0:3] =='200':
        
        if ParameterOne == 'S': #STREAM
            
        #The for loops set all the varibles in the list to FALSE and then
        #Sets the requested mode to true
        
            for i in xrange(0, len(ModeList)):
                ModeList[i] = False
                
            ModeList[0] = True
    
        if ParameterOne == 'C': #COMPRESSION
            
            for i in xrange(0, len(ModeList)):
                ModeList[i] = False
                
            ModeList[1] = True
        
        if ParameterOne == 'B': #BLOCK
        
            for i in xrange(0, len(ModeList)):
                ModeList[i] = False
            
            ModeList[2] = True
 
    return

def makeDirectory(Message):
    #written by Carel Ross 1106684
    #This function implements the MKD command by the Client
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

def removeDirectory(Message):
    #Wrttien by Arlo Eardley 1108472
    #This function implements the RMD command by the Client
     
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

def changeToParentDirectory(Message):
    #written by Carel Ross 1106684
    #This function implements the CDUP command by the Client
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

def deleteFileInDirectory(Message):
    #Wrttien by Arlo Eardley 1108472
    #This function implements the DELE command by the Client
         
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

def changeWorkingDirectory(Message):
    #written by Carel Ross 1106684
    #This function implements the CWD command by the Client    
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

def sendCompressionMode(File,FileTransferSocket):
    #Wrttien by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function implements the sending of data in compression mode
           
    File = File.read() #read all contents of file
    
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
                    
                 FileTransferSocket.send(Block)
                 
                 start = start + 127
                 counter = counter - 127
                 
                if counter > 0 and counter < 127:
                    
                    #Format a block of unique characters less than 127 in length
                    
                    Block = ('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8))                
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    FileTransferSocket.send(Block)
                    
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
                    
                    FileTransferSocket.send(Block)
                    NumberBlocks = NumberBlocks - 63
                    
                #If there are left over for the repeating sequences format them with their number of occurance                    
                if NumberBlocks > 0 and NumberBlocks < 63:
                    
                    Block = ('10' + Number2bits(NumberBlocks,6) + str(string2bits(DataToCompress[i],8)))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    FileTransferSocket.send(Block)
                    
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
                    
         FileTransferSocket.send(Block)
         
         start = start + 127
         counter = counter - 127
         
        if counter > 0 and counter < 127:

            Block = ('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8))
            
            if TypeList[0] == True:
                Block.encode('UTF-8')

            if TypeList[1] == True:
                Block.encode('cp500')
                    
            FileTransferSocket.send(Block)
            
    return

def receiveCompressionMode(FileTransferSocket,IncommingData,File):
    #Wrttien by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function allows the receiving of data in compression mode
    
    #Initalise some variables      
    Binary = IncommingData
    #perform type checks
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

         Number = int(Header[2:],2)# find the number of repeated characters

         i =0

         while i < Number:
             
             Block = chr(int(Binary[k+9:k+16],2))    
             #Write sequence to the file             
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
            
            Number = int(Header[2:],2)
            i =0
            while i<Number:
                
                Block = chr(int(Binary[k+9:k+16],2))
                File.write(Block)
                
                i += 1
            Number = 0
            
        Header = Binary[k+Number*8 +8 : k+Number*8 + 16] 
        k += Number*8 + 8
        
        if k == LengthOfDAta:
            break
            
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


def ChangePort(Message): 
    #written by Carel Ross 1106684
    #This function implements the PORT command for the client
    #the host and port are returned fo that the makeDataConnection()
    #function can actually create the connection
    
    DataHost, DataPort = (Message.replace(Message[0:5],'')).split(' ')

    #format the Host and Port to be able to send in x,x,x,x,y,y format
    Host = str(DataHost).replace('.', ',')
    Port = hex(int(DataPort))[2:]
    PortChange = str(Host) + ',' + str(int(Port[0:2],16)) + ','+ str(int(Port[2:],16))

    Message = ('PORT ' + PortChange +'\r\n')
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print(Reply)
    
    DataPort = int(DataPort)

    return DataHost,DataPort
   
def sendBlockMode(File,FileTransferSocket,MarkerPosition=0):     
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
    
def receiveBlockMode(File,FileTransferSocket,IncommingData,MarkerPosition=0):
    #Wrttien by Arlo Eardley 1108472
    #written by Carel Ross 1106684
    #This function implements the receiving of information in block mode
    #The following headers have been used in this implementation
    #64(01000000) is EOF ----------> done
    #16(00010000) is marker ---------->done
    
    Data = IncommingData
    Number = 0
    
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
            
            #then it is EOF
            Number = int(Header[8:25],2)#extract the length of the data to follow 
            
            #convert data from binary string to charcaters again and write to file
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, len(Data), 8)))
            File.close()
            break
        
        #There are no EOR/Markers
        if Header[0:8] == '00000000':
            

            Number = int(Header[8:25],2)+1#extract the length of the data to follow
            
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


def formatCommands(Message):
    #This function formats the commands sent by the client should the client also
    #require the parameters used
    
    CoammndsNoParam=['QUIT','NOOP','PASV','CDUP', 'PWD']
    CommandsOneParam = ['USER','PASS','RETR','STOR','MKD','RMD','HELP','LIST','TYPE','MODE','DELE','CWD']
    ParameterOne = ''

#format the message with the terminating charcaters\r\n to send to the server
    if Message[0:4] in CoammndsNoParam:
        Message = Message +'\r\n'
        
    if Message[0:3] in CoammndsNoParam:
        Message = Message +'\r\n'
    
    if Message[0:4] in CommandsOneParam:
        
        #Obtain parameter by including whitespace in the removal
        ParameterOne = Message.replace(Message[0:5],'')
        #Format the message to send to Server
        Message = Message + '\r\n'
    
    #Special case for three char commands
    if Message[0:3] in CommandsOneParam:
        
        #Obtain parameter by including whitespace in the removal
        ParameterOne = Message.replace(Message[0:4],'')
        #Format the message to sen to Server
        Message = Message + '\r\n'
   
    return Message, ParameterOne


def printWorkingDir(Message):
    #written by Carel Ross 1106684
    #This function implements the PWD command to send to server
    
    Message,_ = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

def makeDataConnection(Message):
    #This function physically creates the data connection to the server
    #from the Host and Port acquired from the PASV or PORT commands
    
    if PortList[0] == True:
        DataHost,DataPort = passiveMode()
        
        print('The current port and host is: (' + str(DataHost)+ ' ' +str(DataPort) +' )')
        
        FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            #Tries to connect using PASV but throws exception if the port is unaviable
            
            FileTransferSocket.connect((DataHost,int(DataPort)))
        
        except socket.error, e:
            print ("Unable to make data connection: %s" % e)
        

    if PortList[1] == True:
        #Create the data connection if the PORT mode had been selected
        
        DataHost,DataPort = ChangePort(Message)
        
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Socket.bind((DataHost,DataPort))
        Socket.listen(5)
        DataConnection, DataAddress = Socket.accept()
        FileTransferSocket = DataConnection
        
    return FileTransferSocket

#login process ia always called first
Login(port,Host)

Message = ''

while 1:
    
    #Take in client input for command to server
    Message = raw_input('Message from client: ')
     
    #Check if the command complies with any of the supported client commands
    
    if Message[0:4] == 'PORT':
        
        PortList[0] = False
        PortList[1] = True
        FileTransferSocket = makeDataConnection(Message)
        continue
    
    if Message[0:4] == 'NOOP':

        NoOperation(Message)
        continue
  
    if Message[0:4] == 'PASV':
        
        PortList[0] = True
        PortList[1] = False
        FileTransferSocket = makeDataConnection(Message)
        continue
    
    if Message[0:4] == 'RETR':
        
          Retrieve(Message,TypeList,FileTransferSocket)
          continue
          
    if Message[0:4] == 'STOR':
        
        Store(Message,TypeList,FileTransferSocket)
        continue
    
    if Message[0:4] == 'LIST':

        getList(Message,FileTransferSocket)
        continue
    
    if Message[0:4] == 'HELP':
        
        getHelp(Message)
        continue
    
    if Message[0:4] =='TYPE':
    
        changeType(Message,TypeList)
        continue
    
    if Message[0:4] == 'MODE':
        
        changeMode(Message,ModeList)
        continue
    
    if Message[0:3] == 'MKD':
        
        makeDirectory(Message)
        continue
    
    if Message[0:3] == 'RMD':
        
        removeDirectory(Message)
        continue
    
    if Message[0:4] == 'CDUP':
        
        changeToParentDirectory(Message)
        continue
    
    if Message[0:4] == 'DELE':
        
        deleteFileInDirectory(Message)
        continue
    
    if Message[0:3] == 'CWD':
        
        changeWorkingDirectory(Message)
        continue
    
    if Message[0:3] == 'PWD':
        printWorkingDir(Message)
        continue
    
    if Message == 'QUIT':
        
        quitService(Message)
        break
  
    else:
        
        #Otherwise the command is unrecognised 
        print (str(Message) + ' is not recognized, please format commands in CAPS')
        
ControlSocket.close()