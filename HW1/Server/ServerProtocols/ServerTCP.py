import socket
import threading
import struct 


#####
ZERO = 0
ONE = 1 
ACK = "ACK"
####

class ThreadedServerTCP(object):
    def __init__(self, host, port, mechanism, prefix_size):
        self.host = host
        self.port = port
        self.mechanism = mechanism
        self.prefix_size = prefix_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ONE)
        self.sock.bind((self.host, self.port))
        self.total_bytes = ZERO
        self.total_messages = ZERO

    def listen(self):
        self.sock.listen(5)
        try:
            while True:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target = self.listenToClient,args = (client,address)).start()
        except (KeyboardInterrupt, SystemExit):
                print("Protocol used: TCP, total messages received : %d, total bytes received: %d"%(self.total_messages, self.total_bytes))
                self.sock.close()

    def receive_data_streaming(self, client):
         while True:
            try:
                data = client.recv(self.prefix_size)
                #print(data)
                if data:
                    self.total_messages += ONE
                    self.total_bytes += len(data)
                else: 
                    raise error('Client disconnected')
            except:
                client.close()
                return False

    def receive_data_stop_and_wait(self, client):
         while True:
            try:
                data = client.recv(self.prefix_size)
                if data:
                    # Set the response to echo back the recieved data 
                    #print(data)
                    self.total_messages += ONE
                    self.total_bytes += len(data)
                    client.send(bytes("ACK","utf-8"))
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False


    def listenToClient(self, client, address):
        print("Client connected")
        if self.mechanism=="STREAM":
            self.receive_data_streaming(client)
        elif self.mechanism=="STOP":
            self.receive_data_stop_and_wait(client)
    
       


