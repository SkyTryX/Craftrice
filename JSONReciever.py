import os 
from socket import * 
addr = ("127.0.0.1", 13000) 
UDPSock = socket(AF_INET, SOCK_DGRAM) 
UDPSock.bind(addr) 
print("Waiting to receive messages...")
while True: 
    (data, addr) = UDPSock.recvfrom(1024) 
    print("Received message: " + data)
    if data == "exit": 
        break 
UDPSock.close() 
os._exit(0)