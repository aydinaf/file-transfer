# CLIENT SIDE SCRIPT
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Author: Aydin Azari Farhad - 40063330
###############################

from audioop import tostereo
from cmath import log
import re
import socket
import os
import time
import math
from urllib import response

opCodeIndex = 0
fileNameIndex = 1
newFileNameIndex = 2

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
    toSend = (f"{opCode}{FL}{FN}{FS}".encode())
    print(f"ToSend: {toSend}")
    clientSocket.send(toSend)
    with open(fileName, "rb") as file:
        while True:
            buffer = file.read(BUFFER_SIZE)
            print(f"Buffer: {buffer}")
            if not buffer:
                break
            clientSocket.sendall(buffer)
    print("Upload Complete.")
    response = (clientSocket.recv(BUFFER_SIZE)).decode("utf-8")
    if (response[0:3] == "000"):
        print("Server provided OK response. Upload Successful.")
    else:
        print("Server did not provide OK response. Upload Failed.")


def get():
    print("Downloading from server...")


def change(oldfileName, newFileName):
    print(f"Changing {oldfileName} to {newFileName}")
    opCode = "010"
    oFL = (fileNameLength(oldfileName))
    oFN = fileNameToBin(oldfileName)
    nFL = (fileNameLength(newFileName))
    nFN = fileNameToBin(newFileName)
    toSend = bytes(f"{opCode}{oFL}{oFN}{nFL}{nFN}", encoding="utf-8")
    print(f"ToSend: {toSend}")
    clientSocket.send(toSend)
    response = (clientSocket.recv(BUFFER_SIZE)).decode("utf-8")
    if (response[0:3] == "000"):
        print("Server provided OK response. Upload Successful.")
    else:
        print(
            f"Server did not provide OK response. Error {response[0:3]} Upload Failed.")


def help():
    print("Asking for help")
    opCode = "011"
    unused = "00000"
    toSend = (f"{opCode}{unused}".encode())
    print(f"ToSend: {toSend}")
    clientSocket.send(toSend)
    print((clientSocket.recv(BUFFER_SIZE)).decode("utf-8")[5:])


def bye():
    clientSocket.close()
    print("Session terminated.")
    clientSocket.close()
    quit()

# Interprets the user command


def getCmd(splitCmd):
    if (splitCmd[opCodeIndex] == "put"):
        put(splitCmd[fileNameIndex])  # done
    elif (splitCmd[opCodeIndex] == "get"):
        get(splitCmd[fileNameIndex])
    elif (splitCmd[opCodeIndex] == "change"):
        change(splitCmd[fileNameIndex], splitCmd[newFileNameIndex])  # done
    elif (splitCmd[opCodeIndex] == "help"):
        help()  # done
    elif (splitCmd[opCodeIndex] == "bye"):
        bye()  # done
    else:
        print(f"Wrong Operation. \"{splitCmd[opCodeIndex]}\" does not exist.")

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
cmd = "bye"  # input("Client:~\$ ")
# splits user input based on space chars into arrays
splitCmd = cmd.split()

getCmd(splitCmd)

clientSocket.close()
