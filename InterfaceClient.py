import Tkinter

from Tkinter import *
import ttk
import FTP_Client

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
        self.parent.title("File Transfer Protocol")
        self.parent.grid_columnconfigure(0, weight = 1)
        self.parent.grid_rowconfigure(0, weight = 1)
        self.parent.config(background = "#222222")

    def Login_interface(self):

        self.Username_label = Tkinter.Label(self.parent, text = "Username: ")
        self.Username_label.place(x = 250, y = 250, width = 100, height =50)
        self.Username_entry = Tkinter.Entry(self.parent)
        self.Username_entry.place(x = 350, y = 250, width = 100, height =50)
        
        self.Password_label = Tkinter.Label(self.parent, text = "Password: ")
        self.Password_label.place(x = 250, y = 300, width = 100, height =50)
        self.Password_entry = Tkinter.Entry(self.parent)
        self.Password_entry.place(x = 350, y = 300, width = 100, height =50)
        
        self.Login_Button = Tkinter.Button(self.parent, text = "Login", command = self.Check_login)
        self.Login_Button.place(x = 250, y = 350, width = 200, height =50)

        self.Exit_Button = Tkinter.Button(self.parent, text = "Exit", command = self.parent.quit)
        self.Exit_Button.place(x = 250, y = 400, width = 200, height =50)

    def Check_login(self):
        #if FTP_Client.isValidUser
        #    Clear_login()
        #else:
        #    return
        self.Clear_login()

    def Clear_login(self):
        self.Username_label.destroy()
        self.Username_entry.destroy()
        self.Password_label.destroy()
        self.Password_entry.destroy()
        self.Login_Button.destroy()
        self.Exit_Button.destroy()
        self.FTP_interface()

    def FTP_interface(self):
        
        Account = "NewUser"
        NumberOfFiles = "0"
        TotalTransfer = "0"
        CurrentTransfer = "0"
        TotalElapsed = "0"
        CurrentElapsed = "0"
#account - current account logged in with 
        self.Account_Label = Tkinter.Label(self.parent, text = "Account: " + str(Account))
        self.Account_Label.place(x = 0, y = 0, width = 200, height =25)
#serverport - edit
        self.ServerPort_Label = Tkinter.Label(self.parent, text = "Enter alternative server port:")
        self.ServerPort_Label.place(x = 200, y = 0, width = 200, height =25)
        self.ServerPort_Entry = Tkinter.Entry(self.parent)
        self.ServerPort_Entry.place(x = 400, y = 0, width = 200, height =25)
#Hostaddress - edit
        self.HostAddress_Label = Tkinter.Label(self.parent, text = "Enter alternative host address:")
        self.HostAddress_Label.place(x = 200, y = 25, width = 200, height =25)
        self.HostAddress_Entry = Tkinter.Entry(self.parent)
        self.HostAddress_Entry.place(x = 400, y = 25, width = 200, height =25)
#number of files - label
        self.NumberOf_Files_Label = Tkinter.Label(self.parent, text = "Number of files in directory: " + str(NumberOfFiles))
        self.NumberOf_Files_Label.place(x = 0, y = 25, width = 200, height =25)
#logout - button and show other screen
        self.Logout_Button = Tkinter.Button(self.parent, text = "Logout", command = self.parent.quit)
        self.Logout_Button.place(x = 600, y = 25, width = 100, height =25)
#Exit - close
        self.Exit_Button = Tkinter.Button(self.parent, text = "Exit", command = self.parent.quit)
        self.Exit_Button.place(x = 600, y = 0, width = 100, height =25)

#Amount of data transferred - for current transfer and total
        self.DataTransferTotal_Label = Tkinter.Label(self.parent, text = "Total data transferred (Bytes): " + str(TotalTransfer))
        self.DataTransferTotal_Label.place(x = 0, y = 75, width = 350, height =25)
        self.DataTransferCurrent_Label = Tkinter.Label(self.parent, text = "Data transferred in this session (Bytes): " + str(CurrentTransfer))
        self.DataTransferCurrent_Label.place(x = 0, y = 100, width = 350, height =25)
#time elapsed - for current transfer
        self.TotalElapsed_Label = Tkinter.Label(self.parent, text = "Total elapsed transfer time (s): " + str(TotalElapsed))
        self.TotalElapsed_Label.place(x = 350, y = 75, width = 350, height =25)
        self.CurrentElapsed_Label = Tkinter.Label(self.parent, text = "Elapsed transfer time in this session (s): " + str(CurrentElapsed))
        self.CurrentElapsed_Label.place(x = 350, y = 100, width = 350, height =25)

#transfer buttons
        self.Server_To_Client_Button = Tkinter.Button(self.parent, text = ">>", command = self.data_Update)
        self.Server_To_Client_Button.place(x = 250, y = 150, width = 100, height =25)
        self.Client_To_Server_Button = Tkinter.Button(self.parent, text = "<<", command = self.data_Update)
        self.Client_To_Server_Button.place(x = 350, y = 150, width = 100, height =25)


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
        self.server_label.place(x = 0, y = 150, width = 100, height =25)
        self.ServerTree = ttk.Treeview(self.parent, columns=('File Name', 'File Type'))
        self.ServerTree.heading('#0', text = 'File Index')
        self.ServerTree.heading('#1', text = 'File Name')
        self.ServerTree.heading('#2', text = 'File Type')
        self.ServerTree.column('#0', width = 125)
        self.ServerTree.column('#1', width = 125)
        self.ServerTree.column('#2', width = 100)
        self.ServerTree.place(x = 0, y = 200, width = 350, height =500)
        self.ServerTreeview = self.ServerTree

        self.client_label = Tkinter.Label(self.parent, text = "Client")
        self.client_label.place(x = 600, y = 150, width = 100, height =25)
        self.ClientTree = ttk.Treeview(self.parent, columns=('File Name', 'File Type'))
        self.ClientTree.heading('#0', text = 'File Index')
        self.ClientTree.heading('#1', text = 'File Name')
        self.ClientTree.heading('#2', text = 'File Type')
        self.ClientTree.column('#0', width = 125)
        self.ClientTree.column('#1', width = 125)
        self.ClientTree.column('#2', width = 100)
        self.ClientTree.place(x = 350, y = 200, width = 350, height =500)
        self.ClientTreeview = self.ClientTree

        self.Progress = ttk.Progressbar(self.parent, orient=HORIZONTAL, length=200, mode='determinate')
        self.Progress.place(x = 0, y = 175, width = 700, height =25)
        #self.Progress = pack(side = "bottom")
        self.Progress.start()

        self.i = 1

    def data_Update(self):
        self.ServerTreeview.insert('', 'end', text = "File_"+str(self.i), values = (self.account_entry.get(), self.number_Files_entry.get()))
        self.ClientTreeview.insert('', 'end', text = "File_"+str(self.i), values = (self.account_entry.get(), self.number_Files_entry.get()))
        self.i = self.i + 1



#Label Server, Client
def main():
    root = Tkinter.Tk()
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(700, 700))
    UserInterface = initialize_Window(root)
    root.mainloop()

if __name__=="__main__":
    main()