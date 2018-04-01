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
        loginAttempt = test.ftp().isValidUser(self.Username, self.Password, Host, Port)
        if loginAttempt == '230':
            self.Clear_login()
        else:
            self.Status_label['text'] = loginAttempt
            return

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
        self.Navigate_To_Button.destroy()
        self.Return_From_Button.destroy()
        self.Reply_Code_Label.destroy()
        self.server_label.destroy()
        self.ServerTree.destroy()
        self.ServerTreeview.destroy()
        self.client_label.destroy()
        self.ClientTree.destroy()
        self.ClientTreeview.destroy()
        self.Login_interface()

    def TypeSet(self,value):
        if value == "ASCII":
                test.asciiType().asciiset()                
        if value == "EDCBIC":
                test.edcbicType().edcbicset()
        if value == "IMAGE/BINARY":
                test.ibType().ibset()

    def ModeSet(self,value):
        if value == "STREAM":
                test.streamMode().streamset()                
        if value == "BLOCK":
                test.blockMode().blockset()
        if value == "COMPRESSION":
                test.compressionMode().compressionset()
    def MethodSet(self,value):
        if value == "PASV":
                self.Method = "PASV"
        if value == "PORT":
                self.Method = "PORT"

    def Server_to_Client(self):
        if self.fileName != "?":
                test.ftp().servertoclient(self.fileName, self.Method)
    def Client_to_Server(self):
        if self.fileName != "?":
                test.ftp().clienttoserver(self.fileName, self.Method)
    def Navigate_N(self):
        if self.fileName != "?":
                test.ftp().next(self.fileName)
    def Navigate_P(self):
        if self.fileName != "?":
                test.ftp().previous(self.fileName)
        #fileName = " File Name"
        #update bytes and elapsed time numbers here constantly 
        #self.ServerTreeview.insert('', 'end', text = "File_"+str(self.i), values = (self.account_entry.get(), self.number_Files_entry.get()))
        #self.ClientTreeview.insert('', 'end', text = "File_"+str(self.i), values = (self.account_entry.get(), self.number_Files_entry.get()))
        #self.i = self.i + 1


    def FTP_interface(self):
        Account = self.Username
        #test.ftp().fetchdirectory(Account)
        NumberOfFiles = "0"
        TotalTransfer = "0"
        CurrentTransfer = "0"
        TotalElapsed = "0"
        CurrentElapsed = "0"
        self.Method = "PASV"
        self.fileName = ""
#account - current account logged in with 
        self.Account_Label = Tkinter.Label(self.parent, text = "Account: " + str(Account))
        self.Account_Label.place(x = 0, y = 0, width = 650, height =25)
#Mode and Type
        self.Type_Selected = StringVar(self.parent)
        self.Type_Selected.set("TYPE")
        
        self.Mode_Selected = StringVar(self.parent)
        self.Mode_Selected.set("MODE")

        self.Method_Selected = StringVar(self.parent)
        self.Method_Selected.set("PASV")

        self.Type_Menu = Tkinter.OptionMenu(self.parent, self.Type_Selected, "ASCII", "EDCBIC", "IMAGE/BINARY", command=self.TypeSet)
        self.Type_Menu.place(x = 0, y = 125, width = 350, height =25)
        self.Mode_Menu = Tkinter.OptionMenu(self.parent, self.Mode_Selected, "STREAM", "BLOCK", "COMPRESSION", command=self.ModeSet)
        self.Mode_Menu.place(x = 350, y = 125, width = 350, height =25)
        self.Method_Menu = Tkinter.OptionMenu(self.parent, self.Method_Selected, "PASV", "PORT")
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
        self.Server_To_Client_Button.place(x = 250, y = 175, width = 100, height =25)
        self.Client_To_Server_Button = Tkinter.Button(self.parent, text = "<<", command = self.Client_to_Server)
        self.Client_To_Server_Button.place(x = 350, y = 175, width = 100, height =25)

#navigation buttons
        self.Navigate_To_Button = Tkinter.Button(self.parent, text = "<", command = self.Navigate_P)
        self.Navigate_To_Button.place(x = 100, y = 175, width = 75, height =25)
        self.Return_From_Button = Tkinter.Button(self.parent, text = ">", command = self.Navigate_N)
        self.Return_From_Button.place(x = 175, y = 175, width = 75, height =25)

        self.Reply_Code_Label = Tkinter.Label(self.parent, text = "Server reply code: " + str(NumberOfFiles))
        self.Reply_Code_Label.place(x = 450, y = 175, width = 150, height =25)

#Directory buttons
        self.Parent_Button = Tkinter.Button(self.parent, text = "Parent directory", command = self.Navigate_P)
        self.Parent_Button.place(x = 0, y = 150, width = 175, height =25)
        self.Remove_Button = Tkinter.Button(self.parent, text = "Remove directory", command = self.Navigate_P)
        self.Remove_Button.place(x = 350, y = 150, width = 175, height =25)
        self.Delete_Button = Tkinter.Button(self.parent, text = "Delete file", command = self.Navigate_P)
        self.Delete_Button.place(x = 525, y = 150, width = 175, height =25)
        self.Make_Button = Tkinter.Button(self.parent, text = "Make directory", command = self.Navigate_P)
        self.Make_Button.place(x = 175, y = 150, width = 175, height =25)
        self.NOOP_Button = Tkinter.Button(self.parent, text = "NOOP", command = self.Navigate_P)
        self.NOOP_Button.place(x = 350, y = 100, width = 350, height =25)
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


        self.server_label = Tkinter.Label(self.parent, text = "Server")
        self.server_label.place(x = 0, y = 175, width = 100, height =25)
        self.ServerTree = ttk.Treeview(self.parent, columns=('Server File Name'))
        self.ServerTree['show'] = 'headings'
        self.ServerTree.heading('#1', text = 'Server - File Name')
        self.ServerTree.column('#1', width = 350)
        self.ServerTree.place(x = 0, y = 200, width = 350, height =500)
        self.ServerTreeview = self.ServerTree

        self.client_label = Tkinter.Label(self.parent, text = "Client")
        self.client_label.place(x = 600, y = 175, width = 100, height =25)
        self.ClientTree = ttk.Treeview(self.parent, columns=('Client File Name'))
        self.ClientTree['show'] = 'headings'
        self.ClientTree.heading('#1', text = 'Client - File Name')
        self.ClientTree.column('#1', width = 350)
        self.ClientTree.place(x = 350, y = 200, width = 350, height =500)
        self.ClientTreeview = self.ClientTree

        ClientList = test.ftp().clientDirectory()
        self.i = 0
        for row in ClientList:
                self.ClientTreeview.insert('', str(self.i), values=row)
                self.i += 1

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