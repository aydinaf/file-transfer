# CLIENT SIDE SCRIPT
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Aydin Azari Farhad - 40063330
############## Imports ##################
import math
import time
import socket
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 15000
# receive 4096 bytes each time
BUFFER_SIZE = 4096
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f">>> Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] {address} is connected.")
received = (client_socket.recv(BUFFER_SIZE)).decode("utf-8")
print(f"received: {received}")
print(f"OpCode: {received[0:3]}")

if (received[0:3]) == "000":
    print("it's a put Operator")
    FL = int(received[3:8], 2)
    print(f"FL: {FL}")

    FN = (((received[8:(FL*8)])))
    print(FN)
    a =[]
    for i in range(math.ceil(len(FN)/8)):
        a.append(int(FN[i*8:i*8+8]))

    def toString(a):
        l=[]
        m=""
        for i in a:
            b=0
            c=0
            k=int(math.log10(i))+1
            for j in range(k):
                b=((i%10)*(2**j))   
                i=i//10
                c=c+b
            l.append(c)
        for x in l:
            m=m+chr(x)
        return m

    print(toString(a))


    FS = (received[(8+FL*8):(len(received))])
    print(f"FS: {(int(FS, 2))}")