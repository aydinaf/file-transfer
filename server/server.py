# Server Side Script
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Aydin Azari Farhad - 40063330
############## Imports ##################
from audioop import tostereo
from ctypes import sizeof
import math
import opcode
import time
import socket
import os

# def reciever():
#     print()
# def interpret():
#     print()

debugFlag = 0

SERVER_HOST = input("Please enter server IP address: ")  # "0.0.0.0"
SERVER_PORT = int(input("Please enter port number: "))  # 15000
debugFlag = input("Client: Debug 0 or 1 :~\$ ")
# Set buffer size to 4 Bytes
BUFFER_SIZE = 4096

def debug(message):
    if(debugFlag == 1):
        print(message)

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
while True:
    s.listen(5)
    print(f">>> Listening as {SERVER_HOST}:{SERVER_PORT}")
    client_socket, address = s.accept()
    print(f"[+] {address} is connected. Socket: {client_socket}")

    received = (client_socket.recv(BUFFER_SIZE)).decode("utf-8")
    if(debugFlag):print(f"received: {received}")
    #print(f"OpCode: {received[0:3]}")
    # put()
    if (received[0:3]) == "000":
        print("Recieved a PUT request")
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

        #print(FNstr)

        FS = (received[(8+FL*8):(len(received))])
        #print(f"FS: {(int(FS, 2))}")

        FScount = int(FS, 2)

        # Write file from incoming stream
        with open(FNstr, "wb") as file:
            while True:
                buffer = (client_socket.recv(BUFFER_SIZE))
                file.write(buffer)
                FScount -= len(buffer)
                if (FScount <= 0):
                    # Upload Completed
                    toSend = (f"00000000").encode()
                    client_socket.send(toSend)
                    if(debugFlag):print(f"Sending OK response: {toSend}")
                    break
        print(f"File {FNstr} recieved and created.")
        print(
            f"Expected size: {int(FS, 2)}\tRecieved size: {os.path.getsize(FNstr)}")

    # get()
    elif ((received[0:3]) == "001"):
        print("Change request.")
        FL = int(received[3:8], 2)
        #print(f"FL: {FL}")
        FN = (((received[8:(((FL+1)*8))])))
        #print(f"FN: {FN}")
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
        #print(f"FNstr: {FNstr}")

        try:
            FS = bin(os.path.getsize(FNstr))[2:].zfill(32)

            print("Uploading to client...")
            opCode = "001"
            FL = received[3:8]
            toSend = (f"{opCode}{FL}{FN}{FS}".encode())
            if(debugFlag):print(f"ToSend: {toSend}")
            client_socket.send(toSend)
            with open(FNstr, "rb") as file:
                while True:
                    buffer = file.read(BUFFER_SIZE)
                    if(debugFlag):print(f"Buffer: {buffer}")
                    if not buffer:
                        client_socket.close()
                        break
                    client_socket.sendall(buffer)
            print("Upload Complete.")

        except OSError as e:
            print(f"{e.errno} ", end='')
            print(e)
            toSend = (f"01000000").encode()
            client_socket.send(toSend)
            if(debugFlag):print(f"Sending error response: {toSend}")

    # help()
    elif ((received[0:3]) == "011"):
        helpText = "Commands: bye change get put"
        toSend = (f"110{len(helpText)}{helpText}").encode()
        if(debugFlag):print(f"to send: {toSend}")
        client_socket.send(toSend)

    # change()
    elif ((received[0:3]) == "010"):
        print("Change request.")

        # oFL and oFN:

        oFL = int(received[3:8], 2)
        #print(f"FL: {oFL}")
        oFN = (((received[8:(((oFL+1)*8))])))
        #print(f"oFN: {oFN}")
        a = []
        for i in range(math.ceil(len(oFN)/8)):
            a.append(int(oFN[i*8:i*8+8]))

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

        oFNstr = toString(a)
        #print(f"oFNstr: {oFNstr}")

        # nFL and nFN:

        nFL = int(received[(8+oFL*8):((8+oFL*8)+8)], 2)
        #print(f"FL: {nFL}")
        nFN = (((received[((8+oFL*8)+8-3):(len(received))])))
        #print(f"oFN: {nFN}")
        a = []
        for i in range(math.ceil(len(nFN)/8)):
            a.append(int(nFN[i*8:i*8+8]))

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

        nFNstr = toString(a)
        #print(f"nFNstr: {nFNstr}")

        try:
            os.rename(oFNstr, nFNstr)
            toSend = (f"00000000").encode()
            client_socket.send(toSend)
            if(debugFlag):print(f"Sending OK response: {toSend}")
        except IOError as e:
            print(f"{e.errno} ", end='')
            print(e)
            toSend = (f"10100000").encode()
            client_socket.send(toSend)
            if(debugFlag):print(f"Sending error response: {toSend}")
    elif(received[0:3] == ""):  # Null op code
        print(f"Null Message.")
    else:  # if wrong opCode
        print(f"Invalid opCode \"{received[0:3]}\"")
        toSend = (f"01100000").encode()
        client_socket.send(toSend)
        if(debugFlag):print(f"Sending error response: {toSend}")
