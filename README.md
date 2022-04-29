# file-transfer
 A pair of client and server Python programs that facilitate transfer of files between the two hosts.

A pair of client-server programs that communicate via Python stream sockets and simulate partially the
file transfer protocol (FTP). The main purpose of these client/server programs is to give the client the ability to
download files from the server directory to the client directory and upload files of any type from the client directory to the
server directory.

Client User Commands:
    put fileName
    get fileName
    change oldFileName newFileName
    help
    \nbye
