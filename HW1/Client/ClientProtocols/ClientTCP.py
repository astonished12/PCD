import socket
import sys
import struct

# Create a TCP/IP socket

# Connect the socket to the port where the server is listening

#####
ZERO = 0
ONE = 1 
ACK = "ACK"
####


class ClientTCP(object):
    def __init__(self,host,port, prefix_size):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.sock.connect(self.server_address)
        self.prefix_size = prefix_size
        
    
    def send_data_streaming(self, filename):
        total_messages = ZERO
        total_bytes = ZERO
        try:          
            # Send data
            with open(filename, 'rb') as f:
                bytesToSend = f.read(self.prefix_size)
                while (bytesToSend):
                    self.sock.send(bytesToSend)
                    total_messages += ONE
                    total_bytes += len(bytesToSend)
                    bytesToSend = f.read(self.prefix_size)
        finally:
            return (total_messages, total_bytes)
            pass

    def send_data_stop_and_wait(self, filename):
        total_messages = ZERO
        total_bytes = ZERO
        try:          
            # Send data
            with open(filename, 'rb') as f:
                bytesToSend = f.read(self.prefix_size)
                while (bytesToSend):
                    self.sock.send(bytesToSend)
                    data = self.sock.recv(8).decode("UTF-8")
                    if data == ACK:
                        total_messages += ONE
                        total_bytes += len(bytesToSend)
                        bytesToSend = f.read(self.prefix_size)           
        finally:
            return (total_messages, total_bytes)         
            pass
pass

