import Tkinter

from Tkinter import *
import ttk

import test
#import FTP_Client
#import FTP_Client

class initialize_Window(Tkinter.Frame):
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()
        LoginStatus = False
        if LoginStatus == False:
            self.Login_interface()
        else:
            self.FTP_interface()

    def initialize_user_interface(self):
        self.parent.title("The Silver Server - File-transfer Application")
        self.parent.grid_columnconfigure(0, weight = 1)
        self.parent.grid_rowconfigure(0, weight = 1)
        self.parent.config(background = "#222222")

    def Login_interface(self):
        self.Status_label = Tkinter.Label(self.parent, text = "")
        self.Status_label.place(x = 250, y = 225, width = 200, height =25)

        self.Host_label = Tkinter.Label(self.parent, text = "Host: ")
        self.Host_label.place(x = 250, y = 250, width = 100, height =25)
        self.Host_entry = Tkinter.Entry(self.parent)
        self.Host_entry.insert(0, '192.168.1.38')
        self.Host_entry.place(x = 350, y = 250, width = 100, height =25)

        self.Port_label = Tkinter.Label(self.parent, text = "Port: ")
        self.Port_label.place(x = 250, y = 275, width = 100, height =25)
        self.Port_entry = Tkinter.Entry(self.parent)
        self.Port_entry.insert(0, '5000')
        self.Port_entry.place(x = 350, y = 275, width = 100, height =25)

        self.Username_label = Tkinter.Label(self.parent, text = "Username: ")
        self.Username_label.place(x = 250, y = 300, width = 100, height =25)
        self.Username_entry = Tkinter.Entry(self.parent)
        self.Username_entry.place(x = 350, y = 300, width = 100, height =25)
        
        self.Password_label = Tkinter.Label(self.parent, text = "Password: ")
        self.Password_label.place(x = 250, y = 325, width = 100, height =25)
        self.Password_entry = Tkinter.Entry(self.parent)
        self.Password_entry.place(x = 350, y = 325, width = 100, height =25)
        
        self.Login_Button = Tkinter.Button(self.parent, text = "Login", command = self.Check_login)
        self.Login_Button.place(x = 250, y = 350, width = 200, height =50)

        self.Exit_Button = Tkinter.Button(self.parent, text = "Exit", command = self.parent.quit)
        self.Exit_Button.place(x = 250, y = 400, width = 200, height =50)

    def Check_login(self):
        
        self.Username = self.Username_entry.get()
        self.Password = self.Password_entry.get()
        Host = self.Host_entry.get()
        Port = self.Port_entry.get()
        """
        loginAttempt = test.ftp().isValidUser(self.Username, self.Password, Host, Port)
        if loginAttempt == '230':
            self.Clear_login()
        else:
            self.Status_label['text'] = loginAttempt
            return
        """
        self.Clear_login()

    def Clear_login(self):
        self.Status_label.destroy()
        self.Host_label.destroy()
        self.Host_entry.destroy()
        self.Port_label.destroy()
        self.Port_entry.destroy()
        self.Username_label.destroy()
        self.Username_entry.destroy()
        self.Password_label.destroy()
        self.Password_entry.destroy()
        self.Login_Button.destroy()
        self.Exit_Button.destroy()
        self.FTP_interface()

    def Clear_Interface(self):
        self.Account_Label.destroy()
        self.Type_Menu.destroy()
        self.Mode_Menu.destroy()
        self.Method_Menu.destroy()
        self.ServerPort_Label.destroy()
        self.ServerPort_Entry.destroy()
        self.HostAddress_Label.destroy()
        self.HostAddress_Entry.destroy()
        self.Logout_Button.destroy()
        self.Exit_Button.destroy()
        self.DataTransferTotal_Label.destroy()
        self.DataTransferCurrent_Label.destroy()
        self.TotalElapsed_Label.destroy()
        self.CurrentElapsed_Label.destroy()
        self.Server_To_Client_Button.destroy()
        self.Client_To_Server_Button.destroy()
        self.Previous_Button.destroy()
        self.Next_Button.destroy()
        self.Reply_Code_Label.destroy()
        self.Parent_Button.destroy()
        self.Remove_Button.destroy()
        self.Delete_Button.destroy()
        self.Make_Button.destroy()
        self.Make_Entry.destroy()
        self.NOOP_Button.destroy()
        self.ServerTree.destroy()
        self.ServerTreeview.destroy()
        self.ClientTree.destroy()
        self.ClientTreeview.destroy()
        self.Login_interface()
        test.ftp().disconnectServer()

    def TypeSet(self,value):
        if value == "ASCII":
                test.ftp().asciiset()                
        if value == "EDCBIC":
                test.ftp().edcbicset()
        if value == "IMAGE/BINARY":
                test.ftp().ibset()

    def ModeSet(self,value):
        if value == "STREAM":
                test.ftp().streamset()                
        if value == "BLOCK":
                test.ftp().blockset()
        if value == "COMPRESSION":
                test.ftp().compressionset()
    def MethodSet(self,value):
        if value == "PASV":
                test.ftp().passiveset()
        if value == "PORT":
                test.ftp().portset(self.HostAddress_Entry.get(), self.ServerPort_Entry.get())

    def Server_to_Client(self):
        if self.fileNameServer != "?":
                test.ftp().servertoclient(self.fileNameServer)
                self.ClientList = test.ftp().clientDirectory()
                self.setClientTree()
    def Client_to_Server(self):
        if self.fileNameClient != "?":
                test.ftp().clienttoserver(self.fileNameClient)
                self.ServerList = test.ftp().currentDirectory()
                self.setServerTree()
    def Navigate_N(self):
        if self.fileNameServer != "?":
                test.ftp().next(self.fileNameServer)
                self.ServerList = test.ftp().currentDirectory()
                self.setServerTree()
    def Navigate_P(self):
                test.ftp().previous()
                self.ServerList = test.ftp().currentDirectory()
                self.setServerTree()
    def Navigate_Parent(self):
                test.ftp().parentdirectory()
                self.ServerList = test.ftp().currentDirectory()
                self.setServerTree()
    def Remove_directory(self):
        if self.fileNameServer != "?":
                test.ftp().removedirectory(self.fileNameServer)
                self.ServerList = test.ftp().currentDirectory()
                self.setServerTree()
    def Make_directory(self):
        self.fileName = self.Make_Entry.get()
        if self.fileName != "?":
                test.ftp().makedirectory(self.fileName)
                self.ServerList = test.ftp().currentDirectory()
                self.setServerTree()
    def Delete_file(self):
        if self.fileNameServer != "?":
                test.ftp().deletefile(self.fileNameServer)
                self.ServerList = test.ftp().currentDirectory()
                self.setServerTree()
    def No_operation(self):
        test.ftp().nooperation()

    def setServerTree(self):
        for i in self.ServerTree.get_children():
                self.ServerTree.delete(i)
        self.ServerList = test.ftp().currentDirectory()
        self.i = 0
        for row in self.ServerList:
                self.ServerTreeview.insert('', str(self.i), values=row)
                self.i += 1

    def setClientTree(self):
        for i in self.ClientTree.get_children():
                self.ClientTree.delete(i)
        self.ClientList = test.ftp().clientDirectory()
        self.i = 0
        for row in self.ClientList:
                self.ClientTreeview.insert('', str(self.i), values=row)
                self.i += 1

    
    def selectClientItem(self, event):
        selectedItem = self.ClientTree.focus()
        itemValue = self.ClientTree.item(selectedItem,'values')
        itemText = ''
        for i in itemValue:
                itemText = itemText + ' ' + i
        self.fileNameClient = itemText

    def selectServerItem(self, event):
        selectedItem = self.ServerTree.focus()
        itemValue = self.ServerTree.item(selectedItem,'values')
        itemText = ''
        for i in itemValue:
                itemText = itemText + ' ' + i
        self.fileNameServer = itemText

    def FTP_interface(self):
        Account = self.Username
        #test.ftp().fetchdirectory(Account)
        NumberOfFiles = "0"
        TotalTransfer = "0"
        CurrentTransfer = "0"
        TotalElapsed = "0"
        CurrentElapsed = "0"
        self.fileName = ""
        self.fileNameClient = ""
        self.fileNameServer = ""
#account - current account logged in with 
        self.Account_Label = Tkinter.Label(self.parent, text = "Account: " + str(Account))
        self.Account_Label.place(x = 0, y = 0, width = 650, height =25)
#Mode and Type
        self.Type_Selected = StringVar(self.parent)
        self.Type_Selected.set("ASCII")
        
        self.Mode_Selected = StringVar(self.parent)
        self.Mode_Selected.set("STREAM")

        self.Method_Selected = StringVar(self.parent)
        self.Method_Selected.set("PASV")

        self.Type_Menu = Tkinter.OptionMenu(self.parent, self.Type_Selected, "ASCII", "EDCBIC", "IMAGE/BINARY", command=self.TypeSet)
        self.Type_Menu.place(x = 0, y = 125, width = 350, height =25)
        self.Mode_Menu = Tkinter.OptionMenu(self.parent, self.Mode_Selected, "STREAM", "BLOCK", "COMPRESSION", command=self.ModeSet)
        self.Mode_Menu.place(x = 350, y = 125, width = 350, height =25)
        self.Method_Menu = Tkinter.OptionMenu(self.parent, self.Method_Selected, "PASV", "PORT", command = self.MethodSet)
        self.Method_Menu.place(x = 350, y = 25, width = 300, height = 25)
#serverport - edit
        self.ServerPort_Label = Tkinter.Label(self.parent, text = "Server port:")
        self.ServerPort_Label.place(x = 350, y = 75, width = 150, height =25)
        self.ServerPort_Entry = Tkinter.Entry(self.parent)
        self.ServerPort_Entry.place(x = 500, y = 75, width = 250, height =25)
#Hostaddress - edit
        self.HostAddress_Label = Tkinter.Label(self.parent, text = "Host address:")
        self.HostAddress_Label.place(x = 350, y = 50, width = 150, height =25)
        self.HostAddress_Entry = Tkinter.Entry(self.parent)
        self.HostAddress_Entry.place(x = 500, y = 50, width = 250, height =25)
#number of files - label
        #self.NumberOf_Files_Label = Tkinter.Label(self.parent, text = "IP: " + str(NumberOfFiles))
        #self.NumberOf_Files_Label.place(x = 0, y = 25, width = 200, height =25)
#logout - button and show other screen
        self.Logout_Button = Tkinter.Button(self.parent, text = "Logout", command = self.Clear_Interface)
        self.Logout_Button.place(x = 650, y = 25, width = 50, height =25)
#Exit - close
        self.Exit_Button = Tkinter.Button(self.parent, text = "Exit", command = self.parent.quit)
        self.Exit_Button.place(x = 650, y = 0, width = 50, height =25)

#Amount of data transferred - for current transfer and total
        self.DataTransferTotal_Label = Tkinter.Label(self.parent, text = "Total data transferred (Bytes): " + str(TotalTransfer))
        self.DataTransferTotal_Label.place(x = 0, y = 25, width = 350, height =25)
        self.DataTransferCurrent_Label = Tkinter.Label(self.parent, text = "Data transferred in this session (Bytes): " + str(CurrentTransfer))
        self.DataTransferCurrent_Label.place(x = 0, y = 50, width = 350, height =25)
#time elapsed - for current transfer
        self.TotalElapsed_Label = Tkinter.Label(self.parent, text = "Total elapsed transfer time (s): " + str(TotalElapsed))
        self.TotalElapsed_Label.place(x = 0, y = 75, width = 350, height =25)
        self.CurrentElapsed_Label = Tkinter.Label(self.parent, text = "Elapsed transfer time in this session (s): " + str(CurrentElapsed))
        self.CurrentElapsed_Label.place(x = 0, y = 100, width = 350, height =25)

#transfer buttons
        self.Server_To_Client_Button = Tkinter.Button(self.parent, text = ">>", command = self.Server_to_Client)
        self.Server_To_Client_Button.place(x = 150, y = 175, width = 200, height =25)
        self.Client_To_Server_Button = Tkinter.Button(self.parent, text = "<<", command = self.Client_to_Server)
        self.Client_To_Server_Button.place(x = 350, y = 175, width = 200, height =25)

#navigation buttons
        self.Previous_Button = Tkinter.Button(self.parent, text = "<", command = self.Navigate_P)
        self.Previous_Button.place(x = 0, y = 175, width = 75, height =25)
        self.Next_Button = Tkinter.Button(self.parent, text = ">", command = self.Navigate_N)
        self.Next_Button.place(x = 75, y = 175, width = 75, height =25)

        self.Reply_Code_Label = Tkinter.Label(self.parent, text = "Server reply code: " + str(NumberOfFiles))
        self.Reply_Code_Label.place(x = 550, y = 175, width = 150, height =25)

#Directory buttons
        self.Parent_Button = Tkinter.Button(self.parent, text = "Parent directory", command = self.Navigate_Parent)
        self.Parent_Button.place(x = 0, y = 150, width = 175, height =25)
        self.Remove_Button = Tkinter.Button(self.parent, text = "Remove directory", command = self.Remove_directory)
        self.Remove_Button.place(x = 175, y = 150, width = 175, height =25)
        self.Delete_Button = Tkinter.Button(self.parent, text = "Delete file", command = self.Delete_file)
        self.Delete_Button.place(x = 350, y = 150, width = 175, height =25)
        self.Make_Button = Tkinter.Button(self.parent, text = "Make directory", command = self.Make_directory)
        self.Make_Button.place(x = 350, y = 100, width = 175, height =25)
        self.Make_Entry = Tkinter.Entry(self.parent)
        self.Make_Entry.place(x = 525, y = 100, width = 175, height =25)
        self.NOOP_Button = Tkinter.Button(self.parent, text = "NOOP", command = self.No_operation)
        self.NOOP_Button.place(x = 525, y = 150, width = 175, height =25)
            #def selectItem(a):
            #    curItem = tree.focus()
            #    print tree.item(curItem)

            
            #def edit():
            #    x = tree.get_children()
            #    for item in x: ## Changing all children from root item
            #        tree.item(item, text="blub", values=("foo", "bar"))

            #def delete():
            #    selected_item = tree.selection()[0] ## get selected item
            #    tree.delete(selected_item)

            #tree.bind('<ButtonRelease-1>', selectItem)

            #{'text': 'Name', 'image': '', 'values': [u'Date', u'Time', u'Loc'], 'open': 0, 'tags': ''}


        self.ServerTree = ttk.Treeview(self.parent, columns=('Server File Name'))
        self.ServerTree['show'] = 'headings'
        self.ServerTree.heading('#1', text = 'Server - File Name')
        self.ServerTree.column('#1', width = 350)
        self.ServerTree.place(x = 0, y = 200, width = 350, height =500)
        self.ServerTreeview = self.ServerTree

        self.ServerTree.bind('<ButtonRelease-1>', self.selectServerItem)

        self.ClientTree = ttk.Treeview(self.parent, columns=('Client File Name'))
        self.ClientTree['show'] = 'headings'
        self.ClientTree.heading('#1', text = 'Client - File Name')
        self.ClientTree.column('#1', width = 350)
        self.ClientTree.place(x = 350, y = 200, width = 350, height =500)
        self.ClientTreeview = self.ClientTree

        self.ClientTree.bind('<ButtonRelease-1>', self.selectClientItem)

        self.setClientTree()
        self.setServerTree()


#Label Server, Client
def main():
    root = Tkinter.Tk()
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(700, 700))
    UserInterface = initialize_Window(root)
    root.mainloop()

if __name__=="__main__":
    main()
"""
TYPES::
ASCII
EDCBIC
IMAGE/Binary

MODES::
STREAM
BLOCK
COMRPESSION

#Type List In order ASCII, EDCBIC, IMAGE
TypeList = [True, False, False]

#Mode list in order of Stream, Compressed, Block
ModeList = [True, False, False]
"""

"""
Message from client: LIST /

227 Entering Passive Mode (127,0,0,1,208,161)
Control connection: 
150 opening data connection...
Data port reply:

bells.txt
hey
lol
Panther.mov
why.txt
YOLO.txt

Control connection:
226 Closing data connection

Message from client:
"""
"""
Message from client: LIST /lol

227 Entering Passive Mode (127,0,0,1,209,31)
Control connection: 
150 opening data connection...
Data port reply:

alright.txt
mkay.txt
ok

Control connection:
226 Closing data connection

Message from client:
"""