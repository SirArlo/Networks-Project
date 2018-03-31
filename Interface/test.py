import FTP_Client
import sys
import os

class ftp(object):
    def isValidUser(self, Username, Password, Host, Port):
        #FTP_Client.Connect().startConnection()
        loginStatus = ''
        if Username != '':
            loginStatus = FTP_Client.Connect().Login(Username, Password, Host, Port)
        else:
            loginStatus = 'Invalid Entry'
        return loginStatus

    def clientDirectory(self):
        Filename = os.path.dirname(os.path.realpath(__file__))
        ListOfDirFiles = os.listdir(Filename)
        sorted(ListOfDirFiles)
        return ListOfDirFiles

    def fetchdirectory(self, fileName):
        print "Current directory " + fileName
        #number of files
    def next(self, fileName):
        print "Next directory " + fileName
        #number of files
    def previous(self, fileName):
        print "Previous directory " + fileName
        #number of files
    def servertoclient(self, fileName):
        #fileName = " NAME"
        print "Transfer: Server to client " + fileName
        #call time elapsed
        #call data transferred
    def clienttoserver(self, fileName):
        #fileName = " NAME"
        print "Transfer: Client to server " + fileName
        #call time elapsed
        #call data transferred

class asciiType(object):
    def asciiset(self):
        print "ASCII type set"

class edcbicType(object):
    def edcbicset(self):
        print "EDCBIC type set"

class ibType(object):
    def ibset(self):
        print "Image/ Binary type set"

class streamMode(object):
    def streamset(self):
        print "Stream mode set"

class blockMode(object):
    def blockset(self):
        print "Block mode set"
 
class compressionMode(object):
    def compressionset(self):
        print "Compression mode set"

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
        