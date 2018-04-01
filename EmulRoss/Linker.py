import FTP_Client
import sys
import os

class ftp(object):
    #Arlo Eardley 1108472 
    def __init__(self):
        self.MethodinUse = 'PASV'
        self.TypeinUse = 'A'
        self.ModeinUse = 'S'
        self.dataHost = ''
        self.dataport = ''
        self.TypeList = [True, False, False]
        self.ModeList = [True, False, False]

    #Arlo Eardley 1108472 
    def disconnectServer(self):
        FTP_Client.Connect().quitService('QUIT')

    #Arlo Eardley 1108472 
    def isValidUser(self, Username, Password, Host, Port):
        loginStatus = ''
        if Username != '':
            loginStatus = FTP_Client.Connect().Login(Username, Password, Host, Port)
        else:
            loginStatus = 'Invalid Entry'
        return loginStatus

    #Carel Ross 1106684
    def clientDirectory(self):
        Filename = os.path.dirname(os.path.realpath(__file__))
        ListOfDirFiles = os.listdir(Filename)
        sorted(ListOfDirFiles)
        return ListOfDirFiles

    #Carel Ross 1106684
    def currentDirectory(self):
        self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
        self.FileTransferSocket =  FTP_Client.Connect().makeDataConnection(self.MethodinUse)
        Reply1, ListOfDirFiles, Reply2 = FTP_Client.Connect().getList('LIST ' + self.currentPath,self.FileTransferSocket)
        return ListofDirFiles, Reply2

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def next(self, fileName):
        if fileName != "":
            print "Next directory " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            reply = FTP_Client.Connect().changeWorkingDirectory('CWD ' + self.currentPath + '/' + fileName)
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def previous(self):
        print "Previous directory"
        self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
        FTP_Client.Connect().changeToParentDirectory('CDUP')
        self.currentPath[1:self.currentPath.rindex('/')-1]
        reply = FTP_Client.Connect().changeWorkingDirectory('CWD ' + self.currentPath)
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def servertoclient(self, fileName):
        if fileName != "":
            print "Transfer: Server to client " + fileName
            self.FileTransferSocket = FTP_Client.Connect().makeDataConnection(self.MethodinUse)
            Reply, IncomingData, ElapsedTime = FTP_Client.Connect().Retrieve('RETR ' + fileName,self.TypeList,self.FileTransferSocket)
            return Reply, IncomingData, ElapsedTime
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def clienttoserver(self, fileName):
        if fileName != "":
            print "Transfer: Client to server " + fileName
            self.FileTransferSocket = FTP_Client.Connect().makeDataConnection(self.MethodinUse)
            Reply, IncomingData, ElapsedTime = FTP_Client.Connect().Store('STOR ' + fileName,self.TypeList,self.FileTransferSocket)
            return Reply, IncomingData, ElapsedTime
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def parentdirectory(self):
        print "Parent directory"
        reply = FTP_Client.Connect().changeToParentDirectory('CDUP')
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def makedirectory(self, fileName):
        if fileName != "":
            print "Make directory " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            reply = FTP_Client.Connect().makeDirectory('MKD ' + self.currentPath + fileName)
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def removedirectory(self, fileName):
        if fileName != "":
            print "Remove directory " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            reply = FTP_Client.Connect().removeDirectory('RMD ' + self.currentPath)
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def deletefile(self, fileName):
        if fileName != "":
            print "Delete file " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            reply = FTP_Client.Connect().deleteFileInDirectory('DELE ' + fileName)
            return reply
        else:
            print "No file selected"

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def nooperation(self):
        reply = FTP_Client.Connect().NoOperation('NOOP')
        print "NOOP"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def asciiset(self):
        self.TypeinUse = 'A'
        reply = FTP_Client.Connect().changeType('TYPE A',self.TypeList)
        self.TypeList[2] = False
        self.TypeList[1] = False
        self.TypeList[0] = True
        print "ASCII type set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def edcbicset(self):
        self.TypeinUse = 'E'
        reply = FTP_Client.Connect().changeType('TYPE E',self.TypeList)
        self.TypeList[2] = False
        self.TypeList[0] = False
        self.TypeList[1] = True
        print "EDCBIC type set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def ibset(self):
        self.TypeinUse = 'I'
        reply = FTP_Client.Connect().changeType('TYPE I',self.TypeList)
        self.TypeList[1] = False
        self.TypeList[0] = False
        self.TypeList[2] = True
        print "Image/ Binary type set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def streamset(self):
        self.ModeinUse = 'S'
        reply = FTP_Client.Connect().changeMode('MODE S',self.ModeList)
        self.ModeList[1] = False
        self.ModeList[2] = False
        self.ModeList[0] = True
        print "Stream mode set"
        return reply

    #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def blockset(self):
        self.ModeinUse = 'B'
        reply = FTP_Client.Connect().changeMode('MODE B',self.ModeList)
        self.ModeList[0] = False
        self.ModeList[1] = False
        self.ModeList[2] = True
        print "Block mode set"
        return reply
 
     #Arlo Eardley 1108472 
    #Carel Ross 1106684
    def compressionset(self):
        self.ModeinUse = 'C'
        reply = FTP_Client.Connect().changeMode('MODE C',self.ModeList)
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
        