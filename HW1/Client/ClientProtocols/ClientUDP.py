
import socket
import sys


#####
ZERO = 0
ONE = 1 
ACK = "ACK"
TIME_OUT = 0.2
####

class ClientUDP(object):
    def __init__(self,host,port, prefix_size):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)
        self.prefix_size = prefix_size
        
    def send_data_streaming(self, filename):
        total_messages = ZERO
        total_bytes = ZERO
        try:          
            # Send data
            with open(filename, 'rb') as f:
                bytesToSend = f.read(self.prefix_size)
                while (bytesToSend):
                    self.sock.sendto(bytesToSend,self.server_address)
                    total_messages += 1
                    total_bytes += len(bytesToSend)
                    bytesToSend = f.read(self.prefix_size)

                
        finally:
            return (total_messages, total_bytes)         
            pass

    def send_data_stop_and_wait(self, filename):
        total_messages = ZERO
        total_bytes = ONE
        self.sock.settimeout(TIME_OUT)
        # Send data
        with open(filename, 'rb') as f:
            bytesToSend = f.read(self.prefix_size)
            while (bytesToSend):
                self.sock.sendto(bytesToSend,self.server_address)
                while 1:
                    self.sock.settimeout(TIME_OUT)
                    try:
                        data,_ = self.sock.recvfrom(3)
                        ack = data.decode("UTF-8")
                        #print(ack)
                        if ack==ACK:
                            pass
                            #print("Received ack from server")
                    except Exception as e:
                        #print("Time out reached, resending ...package")
                        self.sock.sendto(bytesToSend,self.server_address)
                    else:
                        self.sock.settimeout(ZERO)
                        break
                                          
                total_messages += ONE
                total_bytes += len(bytesToSend)
                bytesToSend = f.read(self.prefix_size)

            return (total_messages, total_bytes)         


