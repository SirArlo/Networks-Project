import FTP_Client
import sys
import os
from ast import literal_eval

class ftp(object):
    #Arlo Eardley 1108472 
    def __init__(self):
        self.MethodinUse = 'PORT'
        self.TypeinUse = 'A'
        self.ModeinUse = 'S'
        self.dataHost = '192.168.1.44'
        self.dataPort = '7000'
        self.TypeList = [True, False, False]
        self.ModeList = [True, False, False]
        self.Server = FTP_Client.Connect()

    #Arlo Eardley 1108472 
    def disconnectServer(self):
        self.Server.quitService('QUIT')

    #Arlo Eardley 1108472 
    def isValidUser(self, Username, Password, ServerHost, ServerPort, ClientHost, ClientPort):
        loginStatus = ''
        if Username != '':
            loginStatus = self.Server.Login(Username, Password, ServerHost, ServerPort)
            if ClientHost[0:3] == '192' and ServerHost[0:3] == '192':
                self.MethodinUse = 'PORT ' + ClientHost + ' ' + ClientPort
            if ClientHost[0:3] == '127' and ServerHost[0:3] == '127':
                self.MethodinUse = 'PASV'

        else:
            loginStatus = 'Invalid Entry'
        return loginStatus

    #Carel Ross 1106684
    def clientDirectory(self):
        Filename = os.path.dirname(os.path.realpath(__file__))
        ListOfDirFiles = os.listdir(Filename)
        sorted(ListOfDirFiles)
        print(ListOfDirFiles)
        return ListOfDirFiles

    #Carel Ross 1106684
    def currentDirectory(self):
        self.currentPath = self.Server.printWorkingDir('PWD')
        self.currentPath = (self.currentPath.split('"'))[1].split('"')[0]
        self.FileTransferSocket = self.Server.makeDataConnection(self.MethodinUse)
        Reply1, ListOfDirText, Reply2 = self.Server.getList('LIST ' + self.currentPath,self.FileTransferSocket)
        ListOfDirFiles = ListOfDirText.split('\n')
        for i in ListOfDirFiles:
            if i == '':
                ListOfDirFiles.remove(i)
        print(ListOfDirFiles)
        return ListOfDirFiles, Reply2

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def next(self, fileName):
        if fileName != "":
            print "Next directory " + fileName.replace(' ', '')
            self.currentPath = self.Server.printWorkingDir('PWD')
            self.currentPath = (self.currentPath.split('"'))[1].split('"')[0]
            # + self.currentPath + '/' 
            reply = self.Server.changeWorkingDirectory('CWD ' + fileName.replace(' ', '/'))
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def previous(self):
        print "Previous directory"
        self.currentPath = self.Server.printWorkingDir('PWD')
        self.currentPath = (self.currentPath.split('"'))[1].split('"')[0]
        reply = self.Server.changeToParentDirectory('CDUP')
        self.currentPath = self.currentPath[0:self.currentPath.rindex('/')]
        print 'HELLLLLLLLLLLLLLLLLLLLLLLLLO ' + self.currentPath
        reply = self.Server.changeWorkingDirectory('CWD ' + self.currentPath)
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def servertoclient(self, fileName):
        if fileName != "":
            print "Transfer: Server to client " + fileName
            self.FileTransferSocket = self.Server.makeDataConnection(self.MethodinUse)
            Reply, IncomingData, ElapsedTime = self.Server.Retrieve('RETR' + fileName,self.TypeList,self.FileTransferSocket)
            return Reply, IncomingData, ElapsedTime
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def clienttoserver(self, fileName):
        if fileName != "":
            print "Transfer: Client to server " + fileName
            self.FileTransferSocket = self.Server.makeDataConnection(self.MethodinUse)
            Reply, IncomingData, ElapsedTime = self.Server.Store('STOR' + fileName,self.TypeList,self.FileTransferSocket)
            return Reply, IncomingData, ElapsedTime
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def parentdirectory(self):
        print "Parent directory"
        reply = self.Server.changeToParentDirectory('CDUP')
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def makedirectory(self, fileName):
        if fileName != "":
            print "Make directory " + fileName
            self.currentPath = self.Server.printWorkingDir('PWD')
            self.currentPath = (self.currentPath.split('"'))[1].split('"')[0]
            reply = self.Server.makeDirectory('MKD ' + fileName)
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def removedirectory(self, fileName):
        if fileName != "":
            print "Remove directory " + fileName
            self.currentPath = self.Server.printWorkingDir('PWD')
            self.currentPath = (self.currentPath.split('"'))[1].split('"')[0]
            reply = self.Server.removeDirectory('RMD' + self.currentPath + '/' + fileName)
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def deletefile(self, fileName):
        if fileName != "":
            print "Delete file " + fileName
            self.currentPath = self.Server.printWorkingDir('PWD')
            self.currentPath = (self.currentPath.split('"'))[1].split('"')[0]
            reply = self.Server.deleteFileInDirectory('DELE' + fileName)
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def nooperation(self):
        reply = self.Server.NoOperation('NOOP')
        print "NOOP"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def asciiset(self):
        self.TypeinUse = 'A'
        reply = self.Server.changeType('TYPE A',self.TypeList)
        self.TypeList[2] = False
        self.TypeList[1] = False
        self.TypeList[0] = True
        print "ASCII type set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def edcbicset(self):
        self.TypeinUse = 'E'
        reply = self.Server.changeType('TYPE E',self.TypeList)
        self.TypeList[2] = False
        self.TypeList[0] = False
        self.TypeList[1] = True
        print "EDCBIC type set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def ibset(self):
        self.TypeinUse = 'I'
        reply = self.Server.changeType('TYPE I',self.TypeList)
        self.TypeList[1] = False
        self.TypeList[0] = False
        self.TypeList[2] = True
        print "Image/ Binary type set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def streamset(self):
        self.ModeinUse = 'S'
        reply = self.Server.changeMode('MODE S',self.ModeList)
        self.ModeList[1] = False
        self.ModeList[2] = False
        self.ModeList[0] = True
        print "Stream mode set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def blockset(self):
        self.ModeinUse = 'B'
        reply = self.Server.changeMode('MODE B',self.ModeList)
        self.ModeList[0] = False
        self.ModeList[1] = False
        self.ModeList[2] = True
        print "Block mode set"
        return reply
 
     #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def compressionset(self):
        self.ModeinUse = 'C'
        reply = self.Server.changeMode('MODE C',self.ModeList)
        self.ModeList[2] = False
        self.ModeList[0] = False
        self.ModeList[1] = True
        print "Compression mode set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def passiveset(self):
        self.MethodinUse = 'PASV'
        print self.MethodinUse
        
    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def portset(self, newHost, newPort):
        self.MethodinUse = 'PORT ' + newHost + ' ' + newPort
        self.dataHost = newHost
        self.dataPort = newPort
        print self.MethodinUse

class timeElapsedClass(object):
    def currentSession(self):
        print "Current session time elapsed"
    def totalSession(self):
        print "Total time elapsed"

class dataTransferClass(object):
    def currentSession(self):
        print "Current session data transferred"
    def totalSession(self):
        print "Total data transferred"
        