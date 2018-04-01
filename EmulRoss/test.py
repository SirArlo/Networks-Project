import FTP_Client
import sys
import os

class ftp(object):
    def __init__(self):
        self.MethodinUse = 'PASV'
        self.TypeinUse = 'A'
        self.ModeinUse = 'S'
        self.dataHost = ''
        self.dataport = ''
        self.TypeList = [True, False, False]
        self.ModeList = [True, False, False]

    def disconnectServer(self):
        FTP_Client.Connect().quitService('QUIT')

    def isValidUser(self, Username, Password, Host, Port):
        #FTP_Client.Connect().startConnection()
        loginStatus = ''
        if Username != '':
            loginStatus = FTP_Client.Connect().Login(Username, Password, Host, Port)
        else:
            loginStatus = 'Invalid Entry'
        return loginStatus

        """
        To get the list of directories:

        Call PASV or PORT as mentioned above 

        Call LIST
        Eg LIST /
        Eg LIST 
        Eg LIST /okay/lol

        List is transfered over data connection 


        For STOR RETR LIST the data connection has to be set up before calling these functions or it will break
        """
    def clientDirectory(self):
        Filename = os.path.dirname(os.path.realpath(__file__))
        ListOfDirFiles = os.listdir(Filename)
        sorted(ListOfDirFiles)
        return ListOfDirFiles

    def currentDirectory(self):
        self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
        self.FileTransferSocket =  FTP_Client.Connect().makeDataConnection(self.MethodinUse)
        ListOfDirFiles = FTP_Client.Connect().getList('LIST ' + self.currentPath,self.FileTransferSocket)
        return ListofDirFiles

    def next(self, fileName):
        if fileName != "":
            print "Next directory " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            FTP_Client.Connect().changeWorkingDirectory('CWD ' + self.currentPath + '/' + fileName)
        else:
            print "No file selected"

    def previous(self):
        print "Previous directory"
        self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
        FTP_Client.Connect().changeToParentDirectory('CDUP')
        self.currentPath[1:self.currentPath.rindex('/')-1]
        FTP_Client.Connect().changeWorkingDirectory('CWD ' + self.currentPath)

        #number of files
        """
        To send/receive to/from sever after login:
        Call Mode or Type if needed
        Eg MODE B 
        Eg TYPE E

        Then call the PASV or PORT command 
        Eg PASV 
        Eg PORT 127.0.0.1 7000

        Then call STOR or RETR 
        Eg STOR lol.txt
        Eg RETR lol.txt

        If you need to do another transfer you have to call PASV or PORT again and then STOR or RETR
        """
    def servertoclient(self, fileName):
        #fileName = " NAME"
        if fileName != "":
            print "Transfer: Server to client " + fileName
            self.FileTransferSocket = FTP_Client.Connect().makeDataConnection(self.MethodinUse)
            FTP_Client.Connect().Retrieve('RETR ' + fileName,self.TypeList,self.FileTransferSocket)
        else:
            print "No file selected"

        #call time elapsed
        #call data transferred
    def clienttoserver(self, fileName):
        #fileName = " NAME"
        if fileName != "":
            print "Transfer: Client to server " + fileName
            self.FileTransferSocket = FTP_Client.Connect().makeDataConnection(self.MethodinUse)
            FTP_Client.Connect().Store('STOR ' + fileName,self.TypeList,self.FileTransferSocket)
        else:
            print "No file selected"
        #call time elapsed
        #call data transferred
    def parentdirectory(self):
        print "Parent directory"
        FTP_Client.Connect().changeToParentDirectory('CDUP')
        #call current directory in Interface

    def makedirectory(self, fileName):
        if fileName != "":
            print "Make directory " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            FTP_Client.Connect().makeDirectory('MKD ' + self.currentPath + fileName)
        else:
            print "No file selected"
        #call current directory in Interface
    def removedirectory(self, fileName):
        if fileName != "":
            print "Remove directory " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            FTP_Client.Connect().removeDirectory('RMD ' + self.currentPath)
        else:
            print "No file selected"
        #call current directory in Interface
    def deletefile(self, fileName):
        if fileName != "":
            print "Delete file " + fileName
            self.currentPath = FTP_Client.Connect().printWorkingDir('PWD')
            FTP_Client.Connect().deleteFileInDirectory('DELE ' + fileName)
        else:
            print "No file selected"
        #call current directory in Interface
    def nooperation(self):
        FTP_Client.Connect().NoOperation('NOOP')
        print "NOOP"

    def asciiset(self):
        self.TypeinUse = 'A'
        FTP_Client.Connect().changeType('TYPE A',self.TypeList)
        self.TypeList[2] = False
        self.TypeList[1] = False
        self.TypeList[0] = True
        print "ASCII type set"

    def edcbicset(self):
        self.TypeinUse = 'E'
        FTP_Client.Connect().changeType('TYPE E',self.TypeList)
        self.TypeList[2] = False
        self.TypeList[0] = False
        self.TypeList[1] = True
        print "EDCBIC type set"

    def ibset(self):
        self.TypeinUse = 'I'
        FTP_Client.Connect().changeType('TYPE I',self.TypeList)
        self.TypeList[1] = False
        self.TypeList[0] = False
        self.TypeList[2] = True
        print "Image/ Binary type set"

    def streamset(self):
        self.ModeinUse = 'S'
        FTP_Client.Connect().changeMode('MODE S',self.ModeList)
        self.ModeList[1] = False
        self.ModeList[2] = False
        self.ModeList[0] = True
        print "Stream mode set"

    def blockset(self):
        self.ModeinUse = 'B'
        FTP_Client.Connect().changeMode('MODE B',self.ModeList)
        self.ModeList[0] = False
        self.ModeList[1] = False
        self.ModeList[2] = True
        print "Block mode set"
 
    def compressionset(self):
        self.ModeinUse = 'C'
        FTP_Client.Connect().changeMode('MODE C',self.ModeList)
        self.ModeList[2] = False
        self.ModeList[0] = False
        self.ModeList[1] = True
        print "Compression mode set"

    def passiveset(self):
        self.MethodinUse = 'PASV'
        print self.MethodinUse
        
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
        