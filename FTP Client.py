# -*- coding: utf-8 -*-
#!/usr/bin/python 
"""
Created on Thu Feb 22 17:03:26 2018
@author: eards
"""
import socket
import time
import os


port = 5000
#Host = '127.0.0.1'#'speedtest.tele2.net'#'ftp.mirror.ac.za'  #'66.220.9.50'##'127.0.0.1' #''#'ftp://mirror.ac.za/'
#Host = 'ftp.dlptest.com'
Host = 'localhost'


#Type List In order ASCII, EDCBIC, IMAGE
TypeList = [True, False, False]

#Mode list in order of Stream, Compressed, Block
ModeList = [True, False, False]

ControlSocket = socket.socket()
ControlSocket.connect((Host,port))

##################This works 100 % needs exceptions#################### 
def Login(port,Host): 
    
    #Establish the connection hopefully receiving the 220 Service Ready
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Reply from server:\n' + str(Reply))
    
    ReplyCode = ''
    while 1:
        
        #Username = 'USER dlpuser@dlptest.com'
        #Username = 'anonymous'
        #Username = 'USER Arlo'
        Username = raw_input('Enter user name: ')
        #Username = 'USER ' + Username + '\r\n'
        Message,_ = formatCommands(Username)

        
        ControlSocket.send(Message.encode('UTF-8'))
        ReplyCode = ControlSocket.recv(4096).decode('UTF-8')
        print( 'Reply from server: \n' + str(ReplyCode))
        
        if ReplyCode[0:3] == '331' or ReplyCode[0:3] =='230':
            break
        
    ReplyCode =''
    while 1:
        
        #Password = 'PASS password'
        #Password = 'PASS eiTqR7EMZD5zy7M'
        #Password = raw_input('PASS ')
        Password = raw_input('Enter Password: ')
        Message,_ = formatCommands(Password)

        ControlSocket.send(Message.encode('UTF-8'))
        ReplyCode = ControlSocket.recv(4096).decode('UTF-8')
        print('Reply from server: \n' + str(ReplyCode))
        
        
        if ReplyCode[0:3] == '230':
            break

    return

##################This Wokrs 100%#################
def getList(Message):
    
    Message,_ = formatCommands(Message)
    DataHost,Fileport = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((DataHost,Fileport))
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    
    print('Control connection: \n' + str(Reply))
    
    Reply = FileTransferSocket.recv(4096).decode('UTF-8')
    print('Data port reply:\n ' + str(Reply))
    
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection:\n ' + str(Reply))

    return


##################This Wokrs 100%#################
def NoOperation(Message):
    
    Message = Message +'\r\n'
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')

    if Reply[0:3] == '200':
        
        print(Reply)
        
    else:
        
        print ('Something has gone wrong?')
        print(Reply)
    
    return

##################This Wokrs 100%#################
def passiveMode():
    
    Message,_ = formatCommands('PASV')
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print( '\n' + str(Reply))
    
    start = Reply.find('(')
    end = Reply.find(')')
    Reply = Reply[start+1:end]
    Reply = Reply.split(',')
    DataHost = str(Reply[0]) + '.'+ str(Reply[1]) +'.'+ str(Reply[2]) +'.'+ str(Reply[3])
    DataPort = (int(Reply[4])*256) + int(Reply[5])
    
    print('New host Data Connection: \n' + str(DataHost))
    print('New port Data Connection:\n ' + str(DataPort))
    
    return DataHost,DataPort


def string2bits(s='', bitnumer=8):
    
    List = [bin(ord(x))[2:].zfill(bitnumer) for x in s]
    
    return ''.join(List)


def Number2bits(Number, NoBits):
    
    Number = bin(Number)[2:]
    
    return str(Number).zfill(NoBits)

##################This Wokrs 100%#################
    
def quitService(Message):
    
    Message,_= formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

##################THis works 100%###################
def getHelp(Message):
    
    Message,_ = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    
    Reply = ControlSocket.recv(8192).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    Reply = ControlSocket.recv(8192).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
        
    return

##################This Wokrs 100%#################
def changeType(Message,TypeList):
    
    Message,ParameterOne = formatCommands(Message)

    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    if ParameterOne == 'A':
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
            
        TypeList[0] = True
        
    if ParameterOne == 'E':
        
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
            
        TypeList[1] = True
         
    if ParameterOne == 'I':
    
        for i in xrange(0, len(TypeList)):
            TypeList[i] = False
        
        TypeList[2] = True

    return

#########This works 100 % needs exceptions##################
def Retrive(Message,TypeList,MarkerPosition=0):
    
    Message,Filename = formatCommands(Message)
    
    DataHost,DataPort = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((DataHost,DataPort))
    
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    StartTimer = time.time()

    with open(Filename, 'wb') as File:
        
        if ModeList[0] == True:
            print(str(Filename) + ' has been opened...')
            
            IncommingData = recv_timeout(FileTransferSocket)
            
            if TypeList[0] == True:
                IncommingData.decode('UTF-8')

            if TypeList[1] == True:
                IncommingData.decode('cp500')
                
        if ModeList[1]== True:
            
            sendCompressionMode(File,TypeList,FileTransferSocket)
        
        if ModeList[2] == True:
            
            sendBlockMode(File,TypeList,FileTransferSocket,MarkerPosition)
           
        File.write(IncommingData)
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print (str(Filename) + ' has finished downloading\n')
        print(str(len(IncommingData)/1000) +' kB of data was downloaded in ' +str(ElapsedTime) +' seconds')
        File.close()
        FileTransferSocket.close()
            
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    
    return

#########This works 100 % needs exceptions##################
def Store(Message,TypeList,MarkerPosition=0):
    
    DataHost,DataPort = passiveMode()
    
    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((DataHost,DataPort))
    
    Message,ParameterOne = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    StartTimer = time.time()

    with open(ParameterOne,'rb') as File:
    
        print(str(ParameterOne) + ' has been opened...')
        
        if ModeList[0] == True:
            OutgoingData = File.read(8192)
             
            while (OutgoingData):
                
                if TypeList[0] == True:
                    OutgoingData.encode('UTF-8')
    
                if TypeList[1] == True:
                    OutgoingData.encode('cp500')
                
                FileTransferSocket.send(OutgoingData)
                OutgoingData = File.read(8192)
                
        if ModeList[1]== True:
            
            sendCompressionMode(File,TypeList,FileTransferSocket)
        
        if ModeList[2] == True:
            
            sendBlockMode(File,TypeList,FileTransferSocket,MarkerPosition)
            
            
        StopTimer = time.time()
        ElapsedTime = StopTimer - StartTimer
        print(str(ParameterOne) + ' has been uploaded to the server in'+ str(ElapsedTime) +' seconds')
        FileTransferSocket.close()
        File.close()
        
        Reply = ControlSocket.recv(4096).decode('UTF-8')
        print('Control connection reply: \n' + str(Reply))
    
       
        
    return

#########This works 100 % needs exceptions##################
def changeMode(Message,ModeList):
    
    Message, ParameterOne = formatCommands(Message)
   
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))

    
    if ParameterOne == 'S':
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
            
        ModeList[0] = True

    if ParameterOne == 'C':
        
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
            
        ModeList[1] = True
    
    if ParameterOne == 'B':
    
        for i in xrange(0, len(ModeList)):
            ModeList[i] = False
        
        ModeList[2] = True
 
    return

#########This works 100 % needs exceptions##################
def makeDirectory(Message):
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

#########This works 100 % needs exceptions##################
def removeDirectory(Message):
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

#########This works 100 % needs exceptions##################
def changeToParentDirectory(Message):
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

#########This works 100 % needs exceptions##################
def deleteFileInDirectory(Message):
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return

#########This works 100 % needs exceptions##################
def changeWorkingDirectory(Message):
    
    Message,Pathname = formatCommands(Message)
    
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
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


###########################################################
#################NEEDS TESTING#####################
def ChangePort(host,port,Host): 
    
    #Take text input here from GUI
    FileHost = '127.0.0.1'
    FilePOrt = 7000
    
    host = str(host).replace('.', ',')
    port = hex(port)[2:]
    PortChange = str(host) + ',' + str(int(port[0:2],16)) + ','+ str(int(port[2:],16))
    
    print(PortChange)
    
    Request = 'PORT ' + PortChange + '\r\n'
    
    ControlSocket.send(Request.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    
    print(Reply)
    

    FileTransferSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    FileTransferSocket.connect((FileHost,FilePOrt))
    print('hererere')
    
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    
    print(Reply)
    
    Message = raw_input('Message to server:')
    
    Message = Message +' lol.txt'+ '\r\n'
    ControlSocket.send(Message.encode('UTF-8'))
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))


    File = open('lol.txt','rb')
    Reading = File.read(8192)
    
    while (Reading):
        
        print('reading file')
        FileTransferSocket.send(Reading.encode('UTF-8'))
        Reading = File.read(8192)  
    print('The file has finnished sending to Server')
    
    File.close()
    FileTransferSocket.close()
    
    Reply = ControlSocket.recv(4096).decode('UTF-8')
    print('Control connection reply: \n' + str(Reply))
    
    return PortChange
###################################################
####################################################
################NEEDS TESTING######################
    
def sendCompressionMode(File,TypeList,FileTransferSocket):
           
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
            print( 'counter: ' + str(counter))
            if counter > 0 :
                       
                start = i -counter
                while counter >= 127:

                 print ('Blocktosend')
                 Block  = ('01111111' + string2bits(DataToCompress[start:start + 127],8))
                 #print('01111111' + string2bits(DataToCompress[start:start + 127],8))
                 
                 if TypeList[0] == True:
                     Block.encode('UTF-8')

                 if TypeList[1] == True:
                    Block.encode('cp500')
                    
                 FileTransferSocket.send(Block)
                 
                 start = start + 127
                 counter = counter - 127
                 
                if counter > 0 and counter < 127:

                    print ('Blocktosend') 
                    Block = ('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8))
                    #print('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8)) 
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    FileTransferSocket.send(Block)
                                       
            if Map[i] > 1 and DataToCompress[i] != ' ':
 
                NumberBlocks = Map[i] 
                
                while NumberBlocks >= 63:
                    
                    print ('Compressed')
                    Block = ('10111111' + str(string2bits(DataToCompress[i],8)))
                    #print('10111111' + str(string2bits(DataToCompress[i],8)))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    FileTransferSocket.send(Block)
                    NumberBlocks = NumberBlocks - 63
                    
                if NumberBlocks > 0 and NumberBlocks < 63:
                    
                    print ('Compressed')
                    Block = ('10' + Number2bits(NumberBlocks,6) + str(string2bits(DataToCompress[i],8)))
                    #print('10' + Number2bits(NumberBlocks,6) + str(string2bits(DataToCompress[i],8)))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    FileTransferSocket.send(Block)
                    
            if Map[i] > 1 and DataToCompress[i] == ' ':
               
                NumberBlocks = Map[i] 
                
                while NumberBlocks >= 63:
                    
                    print ('Compressed space')
                    Block = ('11' + Number2bits(NumberBlocks,6))
                    #print('11' + Number2bits(NumberBlocks,6))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    FileTransferSocket.send(Block)
                    NumberBlocks = NumberBlocks - 63
                    
                if NumberBlocks > 0 and NumberBlocks < 63:
                    
                    print ('Compressed space')
                    Block = ('11' + Number2bits(NumberBlocks,6))
                    #print('11' + Number2bits(NumberBlocks,6))
                    
                    if TypeList[0] == True:
                        Block.encode('UTF-8')

                    if TypeList[1] == True:
                        Block.encode('cp500')
                    
                    FileTransferSocket.send(Block)

            counter = 0  
            
        i +=1
        
 ##############end of while loop##################
 
    print( 'counter: ' + str(counter))
    if counter > 0 :
           
        start = i -counter
        print('Start  ' + str(start))
        while counter >= 127:

         print ('Blocktosend')
         Block = ('01111111' + string2bits(DataToCompress[start:start + 127],8)) 
         #print('01111111' + string2bits(DataToCompress[start:start + 127],8))
         if TypeList[0] == True:
             Block.encode('UTF-8')

         if TypeList[1] == True:
            Block.encode('cp500')
                    
         FileTransferSocket.send(Block)
         
         start = start + 127
         counter = counter - 127
         
        if counter > 0 and counter < 127:

            print ('Blocktosend') 
            Block = ('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8))
            #print('0' + Number2bits(counter,7) + string2bits(DataToCompress[start:start + counter],8)) 
            if TypeList[0] == True:
                Block.encode('UTF-8')

            if TypeList[1] == True:
                Block.encode('cp500')
                    
            FileTransferSocket.send(Block)
            
    return
####################################################
################NEEDS TESTING######################
    
def sendBlockMode(File,TypeList,FileTransferSocket,MarkerPosition =0): 
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
        print('Block to send')
        #print('000000001111111111111111' + string2bits(str(File[start:end])))
        Block = ('000000001111111111111111' + string2bits(str(File[start:end])))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        FileTransferSocket.send(Block)

        Block = ('000100000000000000000110' + string2bits(Marker))
        #print('000100000000000000000110' + string2bits(Marker))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        FileTransferSocket.send(Block)
        
        NumberOfBytes - 65535
        start += 65536
        
    if NumberOfBytes > 0 and NumberOfBytes < 65535:
        
        #this must contain the end of file byte
        Block =('01000000' + Number2bits(NumberOfBytes,16) + string2bits(File[start:end+1]))
        #print('01000000' + Number2bits(NumberOfBytes,16) + string2bits(File[start:end+1]))
        
        if TypeList[0] == True:
            Block.encode('UTF-8')

        if TypeList[1] == True:
            Block.encode('cp500')
                    
        FileTransferSocket.send(Block)
    
    return 

####################################################
####################################################


####################################################
################NEEDS TESTING######################
    
def restartBlockMode(MarkerPosition,Message):
    
    #No idea how to do this 
    return

####################################################
####################################################
################NEEDS TESTING######################
def reciveBlockMode(File,TypeList,FileTransferSocket,MarkerPosition=0):
    
    #128 is EOR ----------> No point in this 
    #64 is EOF ----------> done
    #32 is errors -------> no point in this
    #16 marker ---------->done
    
    IncommingData = recv_timeout(FileTransferSocket)
    Data = IncommingData
    
    
    if MarkerPosition !=0:
        
        k = MarkerPosition
        Header = Data[k:k+24]
        
    else:
        Header = Data[0:24]
        k =0
    
    while 1:

        if Header[0:8] == '01000000':
            
            #then it is EOF
            Number = int(Header[8:24],2)
             
            #print(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
            
        if Header[0:8] == '00000000':
            
            #There are no EOR/EOF/Errors/Markers
            Number = int(Header[8:24],2)
            #print(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
            
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
             
            #print(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
            File.write(''.join(chr(int(Data[i:i+8], 2)) for i in range(k + 24, k + Number*8 + 1, 8)))
            
        Header = Data[k + Number*8 + 8 : k + Number*8 + 16] 
        k += Number*8 + 24
            
        if k == len(Data):
            File.close()
            break
    
    return MarkerPosition

####################################################
###############NEEDS COMPLETION#####################
####################################################

def formatCommands(Message):
    
    CoammndsNoParam=['QUIT','NOOP','PASV','CDUP']
    CommandsOneParam = ['USER','PASS','RETR','STOR','MKD','RMD','HELP','LIST','TYPE','MODE','DELE','CWD']
    CommandsTwoParam = ['PORT']
    ParameterOne = ''
     
    if Message[0:4] in CoammndsNoParam:
        Message = Message +'\r\n'
    
    #Relies on the GUI entering a space after the command
    if Message[0:4] in CommandsOneParam:
        
        #Obtain parameter by including whitespace in the removal
        ParameterOne = Message.replace(Message[0:5],'')
        #Format the message to sen to Server
        Message = Message + '\r\n'
    
    #Special case for three char commands
    if Message[0:3] in CommandsOneParam:
        
        #Obtain parameter by including whitespace in the removal
        ParameterOne = Message.replace(Message[0:4],'')
        #Format the message to sen to Server
        Message = Message + '\r\n'
        
    if Message[0:4] in CommandsTwoParam: 
       Message = Message + '\r\n'
       ParameterOne = Message.replace(Message[0:4],'')
       
       
       
    return Message, ParameterOne



Login(port,Host)

Message = ''

while 1:
    
    Message = raw_input('Message from client: ')
    
    if Message[0:4] == 'RETR':
        
          Retrive(Message,TypeList)
          continue
          
    if Message[0:4] == 'STOR':
        
        Store(Message,TypeList)
        continue
        
    if Message[0:4] == 'PORT':
        
        Newport = ChangePort('127.0.0.1',7000,Host)
        ControlSocket.send(Newport.encode('UTF-8'))
        continue
    
    if Message[0:4] == 'NOOP':

        NoOperation(Message)
        continue
    
    if Message[0:4] == 'REST':
        MarkerPosition =0 # default this to 0
        Restart(MarkerPosition) 
        continue
    
    if Message[0:4] == 'LIST':

        getList(Message)
        continue
    
    if Message[0:4] == 'PASV':
        passiveMode()
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
        
        changeToParentDirectory(Message)
        continue
    
    if Message[0:3] == 'CWD':
        
        changeWorkingDirectory(Message)
        continue
    
    if Message == 'QUIT':
        
        quitService(Message)
        break
    
    else:
        
        ReceivedData = ControlSocket.recv(4096).decode('UTF-8')
        print ('Received from server: ' + ReceivedData)
        Message = raw_input('Message from client: ')
        
    
ControlSocket.close()