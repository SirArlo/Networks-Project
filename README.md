Created by Arlo Eardley and Emul Ross

This repo contains a python implementation of an FTP client and server written using low level socket procedures based on two TCP connections. The following commands have been implemeted for the FTP server and client:

QUIT	NOOP	PASV 	CDUP	MKD	CWD
USER 	PASS 	RETR 	STOR  	RMD 	HELP 
LIST 	TYPE 	MODE 	DELE	PORT

With support for Block, Compression and stream MODES as well as ASCII, Image and IBM's EDCBIC data transfer TYPES.

For Python to run on local host set both hosts in the desired cient file to '127.0.0.1' and both the server and 
client ports must be the same.

To run the server and client on seperate end systems, set the host variable in the client file to the IP address 
of the computer the server is running on. Set the host variable in the server script to the IP address of the 
computer the server is running on. Both port values need to be the same.

1.) The following diagram explains how the directory in which the FTP Server.py or FTP Server multithread.py 
files reside needs to be structured. Inside the directory of choice (Docments for example) there needs to be 
folders named after the usernames of the clients (ArloE and EmulRoss for example) and the python server file 
is in this directory too. Inside each of the clients folders there needs to be a text file named 
credentials.txt that contains the Username on the first line of the file and the password on the second line
of the file corresponding to the details of the client folder (see credentials.txt in the folders in the repo).
The login Details for ArloE are USER ArloE and PASS 1. The text files named as FTP commands such as HELP.txt, 
MODE.txt... etc need to be in the same directory as the server file as these text documents include the help 
information for the FTP HELP command.

	+...Documents
		.
		+.../ArloE
		.     .
		.     .
		.     /credentials.txt
		.
		+.../EmulRoss
		.      .
		.      .
		.      /credentials.txt
		.
		./FTP Server.py
		.
		./FTP Server multithread.py

2.) How to use the FTP client (no GUI):

To run the command line client run the FTP Client.py file with the host and port variables changed to a port and host 
to suit your application.

The commands need to be entered according to FTP (commands have to be in all captial letters) with the corresponding
formatting according to the RFC959 documentation. If there is any uncertainty about how a command is enetered, entering 
the HELP comand will bring up the list of supported commands. Further information about a specific command can be 
acquired by typing in HELP`<space>`CommandName. This will bring up the required information about the command the client
reqested, however the <CRLF> charcaters are not entered as the client script takes care of that. For example 
HELP`<space>`MODE will bring up the list of spported modes and how to use them. The only command
entered by the user in the terminal that is different to FTP is the PORT command that is entered as follows:
PORT`<space>`IP-address`<space>`Port-number. The FTP Client.py performs the operations on this input method in order to
send the information to the server in the FTP format. It is just easier for the user to enter the command this way.

3.)How to use the GUI

The files for the GUI are named FTP_Client.py, InterfaceClient.py and Linker.py. Theses files must all reside in the same 
directory and only the InterfaceClient.py file is to be run for the GUI to open.The port and host variables at the top of 
the 
FTP_Client.py file need to be changed for the control connection based on what you 
would like to do.

The commands do not need to be entered. All the necessary commands and connections are automatically done once a 
particular button is selected. The error checking is very limited, so the user has to be very specific when entering 
information such as the host address and port address. When the GUI is launched, the user is presented with a login 
screen. Here the user is required to type in the host address (defaulted to 192.168.1.38), the port address (defaulted to 5000)
, the username and the password. If the username and password are incorrect, the GUI will inform you. The exit button will close 
the GUI. Once logged in the username will be displayed at the top of the GUI. The GUI presents the amount of data transferred in 
the latest transfer and the total amount of data transferred. It will also show the time elapsed in the latest transfer and the 
total time elapsed for data transfers. The user is able to click on the PASV dropdown menu to switch it to PORT. If PORT is active
then the values in the ‘Host address’ and ‘Server port’ will be used. If PASV is active these values will be ignored. To make a 
directory there needs to be text in the block next to the ‘Make directory’ button. The new directory will be named using that text 
and will be created in the current working directory of the server. The ASCII and STREAM dropdown menus determine the TYPE and MODE
that will be used respectively. The ‘Parent directory’ button will change the working directory of the server to the parent directory.
The ‘Remove directory’ and ‘Delete file’ buttons will impact the selected file in the server accordingly. The ‘NOOP’ button will just 
send a no operation command to the server. The ‘<’ and ‘>’ buttons will navigate between files in the server. The ‘>>’ button will send 
the selected file from the server to the client. The ‘<<’ button will send the selected file from the client to the server. The server 
reply code, server tree and client tree will be updated when required automatically.

4.) How to use the FTP Server (same applies for multithreaded version):

The file FTP Server.py or FTP multithreaded Server.py must be run with the port and host variables changed at the 
top of the script to accomodate your speciffic computer and its open ports and IP address. When the client disconnects 
from the normal FTP server the 
server will shut down and will need to be restarted for a new session.














