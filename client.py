# CLIENT SIDE SCRIPT
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Author: Aydin Azari Farhad - 40063330
###############################

import socket, os, time, math

# Default Buffer Size
BUFFER_SIZE = 4096

# takes file name (splitCmd[1]) as input and returns the length of the name of the file in 5 binary digits
def fileNameLength(file):
    return (bin(len(file))[2:].zfill(5))

# takes file name as input and returns the file name as set of bytes
def fileNameToBin(fileName):
    list,m=[],[]
    for i in fileName:
        list.append(ord(i))
    for i in list:
        m.append(((bin(i)[2:].zfill(8))))
    return m

# takes file name as input, and returns the file size in Bytes [Note: NEEDS TO BE 4 BYTES]
def getFileSize(file):
    return (bin(os.path.getsize(file)))[2:].zfill(32)

# Command Fucntions
def put(fileName):
    print("Uploading to server...")
    opCode = "000"
    FL = (fileNameLength(fileName))
    FN = 
    FS = getFileSize(fileName)
    toSend = bytes(f"{opCode}{FL}{FS}", encoding="utf-8")
    clientSocket.sendall(toSend)
    with open(fileName, "rb") as file:
        while True:
            buffer = file.read(BUFFER_SIZE)
            if not buffer:
                break
            clientSocket.sendall(buffer)
    
def get():
    print("Downloading from server...")
def help():
    print("Asking for help")
def bye():
    clientSocket.close()
    print("Session terminated.")
    quit()
###############################

# Takes IP and port number from user
serverIP = "192.168.217.130" #input("Please enter server IP address: ")
port = 15000 #int(input("Please enter port number: "))
clientSocket = socket.socket()

# Establishes server connection
print(f"Establishing Connection to {serverIP} : {port}")
clientSocket.connect((serverIP,port))
print("Connection Established")

# Takes user command
cmd = input("Client:~\$ ")
# splits user input based on space chars into arrays
splitCmd = cmd.split()

# Interprets the user command
def getCmd(splitCmd):
    if ('put' in splitCmd):
        put()
    elif ('get' in splitCmd):
        get()
    elif ('help' in splitCmd):
        help()
    elif ('bye' in splitCmd):
        bye()
