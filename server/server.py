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
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"[+] {address} is connected.")
received = (client_socket.recv(BUFFER_SIZE))
print(received)
print(received.decode("utf-8"))
