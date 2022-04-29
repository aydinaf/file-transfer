# CLIENT SIDE SCRIPT
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Aydin Azari Farhad - 40063330
############## Imports ##################
from audioop import tostereo
import math
import time
import socket
import os


def reciever():
    print()


def interpret():
    print()


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 15000
# Set buffer size to 4 Bytes
BUFFER_SIZE = 4096

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f">>> Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] {address} is connected. Socket: {client_socket}")

received = (client_socket.recv(BUFFER_SIZE)).decode("utf-8")
print(f"received: {received}")
print(f"OpCode: {received[0:3]}")

if (received[0:3]) == "000":
    print("Recieved a PUT request")
    FL = int(received[3:8], 2)
    print(f"FL: {FL}")

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
    print(f"FS: {(int(FS, 2))}")

    # Write file from incoming stream
    with open(FNstr, "wb") as file:
        while True:
            buffer = (client_socket.recv(BUFFER_SIZE))
            if not buffer:
                # Upload Completed
                # client_socket.send("00000000".encode("utf-8"))
                print(
                    f"BREAK... BUFFER = {buffer}. Buffer Length: {len(buffer)}")
                break
            file.write(buffer)
            # print(buffer)
    print(f"File {FNstr} recieved and created.")
    print(f"Expected size: {int(FS, 2)}\tRecieved size: {os.path.getsize(FNstr)}")
elif ((received[0:3]) == "011"):
    helpText = "Commands: bye change get put"
    toSend = (f"011{len(helpText)}{helpText}").encode()
    print(f"to send: {toSend}")
    client_socket.send(toSend)

# TODO: Functionalize the code above
#      DONE: Take file Bytes from client
#      DONE: Write file
#      Send OK Response
#      Debug Flag
#      Other Operations
#      Error Response
