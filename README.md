Created by Arlo Eardley and Emul Ross

This repo contains a python implementation of an FTP client and server written using low level socket procedures based on two TCP connections. the following commands have been implemeted for the FTP server and client:

QUIT	NOOP	PASV 	CDUP	MKD	CWD
USER 	PASS 	RETR 	STOR  	RMD 	HELP 
LIST 	TYPE 	MODE 	DELE	PORT

With support for Block, Cmpression and stream MODES as well as ASCII, Image and IMB's EDCBIC data transfer TYPES.