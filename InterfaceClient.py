import Tkinter

from Tkinter import *
import ttk

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
        self.parent.config(background = "white")

    def Login_interface(self):
        self.parent.title("File Transfer Protocol")
        self.parent.grid_columnconfigure(0, weight = 1)
        self.parent.grid_rowconfigure(0, weight = 1)
        self.parent.config(background = "white")

        self.Username_label = Tkinter.Label(self.parent, text = "Username: ")
        self.Username_entry = Tkinter.Entry(self.parent)
        self.Username_label.grid(row = 0, column = 0, sticky = Tkinter.W)
        self.Username_entry.grid(row = 0, column = 1)
        
        self.Password_label = Tkinter.Label(self.parent, text = "Password: ")
        self.Password_entry = Tkinter.Entry(self.parent)
        self.Password_label.grid(row = 2, column = 0, sticky = Tkinter.W)
        self.Password_entry.grid(row = 2, column = 1)

    def FTP_interface(self):
        self.account_label = Tkinter.Label(self.parent, text = "Account: ")
        self.account_entry = Tkinter.Entry(self.parent)
        self.account_label.grid(row = 0, column = 0, sticky = Tkinter.W)
        self.account_entry.grid(row = 0, column = 1)

        self.number_Files_label = Tkinter.Label(self.parent, text = "Number of files: ")
        self.number_Files_entry = Tkinter.Entry(self.parent)
        self.number_Files_label.grid(row = 1, column = 0, sticky = Tkinter.W)
        self.number_Files_entry.grid(row = 1, column = 1)

        self.exit_button = Tkinter.Button(self.parent, text = "Exit", command = self.parent.quit)
        self.exit_button.grid(row = 0, column = 4)

        self.Server_To_Client_Button = Tkinter.Button(self.parent, text = ">>", command = self.data_Update)
        self.Server_To_Client_Button.grid(row = 6, column = 2, sticky = Tkinter.W, padx = 50)
        self.Client_To_Server_Button = Tkinter.Button(self.parent, text = "<<", command = self.data_Update)
        self.Client_To_Server_Button.grid(row = 7, column = 2, sticky = Tkinter.W, padx = 50)


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
        self.server_label.grid(row = 2, column = 1, sticky = Tkinter.W)
        self.ServerTree = ttk.Treeview(self.parent, columns=('File Name', 'File Type'))
        self.ServerTree.heading('#0', text = 'File Index')
        self.ServerTree.heading('#1', text = 'File Name')
        self.ServerTree.heading('#2', text = 'File Type')
        #self.tree.column('#1', stretch = Tkinter.YES)
        #self.tree.column('#2', stretch = Tkinter.YES)
        #self.tree.column('#0', stretch = Tkinter.YES)
        self.ServerTree.grid(row = 3, rowspan = 14, column = 1)
        self.ServerTreeview = self.ServerTree

        self.client_label = Tkinter.Label(self.parent, text = "Client")
        self.client_label.grid(row = 2, column = 3, sticky = Tkinter.W)
        self.ClientTree = ttk.Treeview(self.parent, columns=('File Name', 'File Type'))
        self.ClientTree.heading('#0', text = 'File Index')
        self.ClientTree.heading('#1', text = 'File Name')
        self.ClientTree.heading('#2', text = 'File Type')
        #self.tree.column('#1', stretch = Tkinter.YES)
        #self.tree.column('#2', stretch = Tkinter.YES)
        #self.tree.column('#0', stretch = Tkinter.YES)
        self.ClientTree.grid(row = 3, rowspan = 14, column = 3)
        self.ClientTreeview = self.ClientTree

        self.Progress = ttk.Progressbar(self.parent, orient=HORIZONTAL, length=200, mode='determinate')
        self.Progress.grid(row = 20, columnspan = 5, sticky = 'nsew')
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
    UserInterface = initialize_Window(root)
    root.mainloop()

if __name__=="__main__":
    main()