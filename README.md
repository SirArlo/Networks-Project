Created by Arlo Eardley and Emul Ross

This repo contains a python implementation of an FTP client and server written using low level socket procedures based on two TCP connections. The following commands have been implemeted for the FTP server and client:

QUIT	NOOP	PASV 	CDUP	MKD	CWD
USER 	PASS 	RETR 	STOR  	RMD 	HELP 
LIST 	TYPE 	MODE 	DELE	PORT

With support for Block, Cmpression and stream MODES as well as ASCII, Image and IMB's EDCBIC data transfer TYPES.

1.) The following diagram explains how the directory in which the FTP Server.py or FTP Server multithread.py 
files reside needs to be structured. Inside the directory of choice (Docments for example) there needs to be 
folders named after the usernames of the clients (ArloE and EmulRoss for example) and the python server file 
is in this directory too. Inside each of the clients folders there needs to be a text file named 
credentials.txt that contains the Username on the first line of the file and the password on the second line
of the file corresponding to the details of the client folder (see credentials.txt in the folders in the repo).

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

2.) How to use the FTP client (no GUI):

The commands need to be entered according to FTP (commands have to be in all captial letters) with the corresponding
formatting according to the RFC959 documentation. If there is any uncertainty about how a command is enetered, entering 
the HELP comand will bring up the list of supported commands. Further information about a specific command can be 
acquired by typing in HELP`<space>`CommandName. This will bring up the required information about the command the client
reqested, however the <CRLF> charcaters are not entered as the client script takes care of that. For example 
HELP`<space>`MODE will bring up the list of spported modes and how to use them. The only command
entered by the user in the terminal that is different to FTP is the PORT command that is entered as follows:
PORT`<space>`IP-address`<space>`Port-number. The FTP Client.py performs the operations on this input method in order to
send the information to the server in the FTP format. It is just easier for the user to enter the command this way.

3.) How to use the FTP Server (same applies for multithreaded version):

The file must be run with the port and host variables changed at the top of the script to accomodate your speciffic
computer and its open ports and IP address. 