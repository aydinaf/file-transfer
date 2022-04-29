# CLIENT SIDE SCRIPT
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Author: Aydin Azari Farhad - 40063330
###############################

from audioop import tostereo
import socket
import os
import time
import math

opCodeIndex = 0
fileNameIndex = 1
newFileNameIndex = 3

# Default Buffer Size
BUFFER_SIZE = 4096

# takes file name (splitCmd[1]) as input and returns the length of the name of the file in 5 binary digits


def fileNameLength(file):
    return (bin(len(file))[2:].zfill(5))

# takes file name as input and returns the file name as set of bytes


def fileNameToBin(fileName):
    name = ''
    for i in fileName:
        name += (bin(ord(i))[2:].zfill(8))
    return name

# takes file name as input, and returns the file size in Bytes
# [Note: NEEDS TO BE 4 BYTES]


def getFileSize(file):
    return (bin(os.path.getsize(file)))[2:].zfill(32)

# Command Fucntions


def put(fileName):
    print("Uploading to server...")
    opCode = "000"
    FL = (fileNameLength(fileName))
    FN = fileNameToBin(fileName)
    FS = getFileSize(fileName)
    toSend = bytes(f"{opCode}{FL}{FN}{FS}", encoding="utf-8")
    print(f"ToSend: {toSend}")
    clientSocket.send(toSend)
    with open(fileName, "rb") as file:
        while True:
            buffer = file.read(BUFFER_SIZE)
            print(f"Buffer: {buffer}")
            if not buffer:
                print("Finished Uploading")
                break
            clientSocket.sendall(buffer)
    print("Upload Complete.")



def get():
    print("Downloading from server...")


def help():
    print("Asking for help")


def bye():
    clientSocket.close()
    print("Session terminated.")
    quit()

# Interprets the user command


def getCmd(splitCmd):
    if ("put" in splitCmd):
        put(splitCmd[fileNameIndex])
    elif ('get' in splitCmd):
        get()
    elif ('help' in splitCmd):
        help()
    elif ('bye' in splitCmd):
        bye()

###############################


# Takes IP and port number from user
serverIP = "192.168.2.18"  # input("Please enter server IP address: ")
port = 15000  # int(input("Please enter port number: "))
clientSocket = socket.socket()

# Establishes server connection
print(f"Establishing Connection to {serverIP} : {port}")
clientSocket.connect((serverIP, port))
print("Connection Established")

# Takes user command
cmd = "put test3.pdf"  # input("Client:~\$ ")
# splits user input based on space chars into arrays
splitCmd = cmd.split()

getCmd(splitCmd)

clientSocket.close()
