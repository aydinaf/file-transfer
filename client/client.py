# CLIENT SIDE SCRIPT
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Author: Aydin Azari Farhad - 40063330
###############################
import socket
import os
import math
import sys

#tempIP = sys.argv[1]
#tempPort = sys.argv[2]

opCodeIndex = 0
fileNameIndex = 1
newFileNameIndex = 2

# Default Buffer Size
BUFFER_SIZE = 4096

# takes file name (splitCmd[1]) as input and returns the length of the name of the file in 5 binary digits

debugFlag = 0
def debug(message):
    if (debugFlag == 1):
        print(message)

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
    FScount = int(FS, 2)
    toSend = (f"{opCode}{FL}{FN}{FS}".encode())
    if(debugFlag):print(f"Uploading to server. Sending: {toSend}")
    clientSocket.send(toSend)
    with open(fileName, "rb") as file:
        while True:
            buffer = file.read(BUFFER_SIZE)
            if(debugFlag):print(f"Buffer: {buffer}")
            print(FScount)
            # if not buffer:
            #     break
            clientSocket.sendall(buffer)
            FScount -= len(buffer)
            if (FScount <= 0):
                # Upload Completed
                break
            print(FScount)
    response = (clientSocket.recv(BUFFER_SIZE)).decode("utf-8")
    if (response[0:3] == "000"):
        print("Server provided OK response. Upload Successful.")
    else:
        print("Server did not provide OK response. Upload Failed.")


def get(fileName):
    print("Downloading from server...")
    opCode = "001"
    FL = (fileNameLength(fileName))
    FN = fileNameToBin(fileName)
    toSend = (f"{opCode}{FL}{FN}".encode())
    if(debugFlag):print(f"ToSend: {toSend}")
    clientSocket.send(toSend)
    received = (clientSocket.recv(BUFFER_SIZE)).decode("utf-8")
    if(debugFlag):print(f"Recieved : {received}")
    if (received[0:3]) == "001":
        FL = int(received[3:8], 2)
        #print(f"FL: {FL}")

        FN = (((received[8:(((FL+1)*8))])))

        a = []
        for i in range(math.ceil(len(FN)/8)):
            a.append(int(FN[i*8:i*8+8]))

        def toString(a):
            l = []
            m = ""
            for i in a:
                b = 0
                c = 0
                k = int(math.log10(i))+1
                for j in range(k):
                    b = ((i % 10)*(2 ** j))
                    i = i // 10
                    c = c + b
                l.append(c)
            for x in l:
                m = m + chr(x)
            return m

        FNstr = toString(a)

        print(FNstr)

        FS = (received[(8+FL*8):(len(received))])
        #print(f"FS: {(int(FS, 2))}")

        # Write file from incoming stream
        with open(FNstr, "wb") as file:
            while True:
                buffer = (clientSocket.recv(BUFFER_SIZE))
                if (not buffer):
                    # Download Completed
                    break
                file.write(buffer)
                #print(buffer)
                if(debugFlag):print(f"Buffer: {buffer}")
                buffer = 0
        print(f"{FNstr} downloaded.")
        print(
            f"Expected size: {int(FS, 2)}\tRecieved size: {os.path.getsize(FNstr)}")


def change(oldfileName, newFileName):
    opCode = "010"
    oFL = (fileNameLength(oldfileName))
    oFN = fileNameToBin(oldfileName)
    nFL = (fileNameLength(newFileName))
    nFN = fileNameToBin(newFileName)
    toSend = bytes(f"{opCode}{oFL}{oFN}{nFL}{nFN}", encoding="utf-8")
    if(debugFlag):print(f"Renaming {oldfileName} to {newFileName}. Sending: {toSend}")
    clientSocket.send(toSend)
    response = (clientSocket.recv(BUFFER_SIZE)).decode("utf-8")
    if(debugFlag):print(f"Response: {response}")
    if (response[0:3] == "000"):
        print("Server provided OK response. Rename Successful.")
    else:
        print(
            f"Server did not provide OK response. Error {response[0:3]} renaming failed.")
    clientSocket.close()


def help():
    opCode = "011"
    unused = "00000"
    toSend = (f"{opCode}{unused}".encode())
    if(debugFlag):print(toSend)
    clientSocket.send(toSend)
    print((clientSocket.recv(BUFFER_SIZE)).decode("utf-8")[5:])
    clientSocket.close()


def bye():
    clientSocket.close()
    print("Session terminated.")
    clientSocket.close()
    quit()

# Interprets the user command


def getCmd(splitCmd):
    if (splitCmd[opCodeIndex] == "put"):
        put(splitCmd[fileNameIndex])
    elif (splitCmd[opCodeIndex] == "get"):
        get(splitCmd[fileNameIndex])
    elif (splitCmd[opCodeIndex] == "change"):
        change(splitCmd[fileNameIndex], splitCmd[newFileNameIndex])
    elif (splitCmd[opCodeIndex] == "help"):
        help()
    elif (splitCmd[opCodeIndex] == "bye"):
        bye()
    else:
        print(f"Wrong Operation. \"{splitCmd[opCodeIndex]}\" does not exist.")

###############################


# Takes IP and port number from user
serverIP = input("Please enter server IP address:~\$ ")  # "192.168.2.18"
port = int(input("Please enter port number:~\$ "))  # 15000  #

# Takes user command
cmd = input("Client:~\$ ")
debugFlag = input("Client: Debug 0 or 1 :~\$ ")
# splits user input based on space chars into arrays
splitCmd = cmd.split()

while True:
    clientSocket = socket.socket()

    # Establishes server connection
    print(f"Establishing Connection to {serverIP} : {port}")
    clientSocket.connect((serverIP, port))
    print("Connection Established")

    getCmd(splitCmd)

    cmd = input("Client:~\$ ")
    splitCmd = cmd.split()

# sys.argv[1,2]
