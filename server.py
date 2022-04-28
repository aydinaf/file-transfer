# CLIENT SIDE SCRIPT
#<><><><><><><><><>#
# COEN366 - Winter 2022
# Project Assignment
# Aydin Azari Farhad - 40063330
############## Imports ##################
import math
import time
import socket, os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 15000
# receive 4096 bytes each time
BUFFER_SIZE = 4096
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)