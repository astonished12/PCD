import socket
import threading
import TCP.tcpClient as Client

#####
ZERO = 0
ONE = 1
####


class ThreadedServerTCP(object):

    def __init__(self, host, port, prefix_size, conn_address =None, conn_port=None):
        self.host = host
        self.port = port
        self.prefix_size = prefix_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ONE)
        self.sock.bind((self.host, self.port))
        self.total_bytes = ZERO
        self.total_messages = ZERO
        self.is_client_too = False
        if conn_address is not None and conn_port is not None:
            self.is_client_too = True
            self.client = Client.ClientTCP(conn_address, conn_port, 2048)

    def listen(self):
        self.sock.listen(5)
        try:
            while True:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target=self.listen_to_client, args=(client, address)).start()
        except (KeyboardInterrupt, SystemExit):
            print("Protocol used: TCP, total messages received : %d, total bytes received: %d" %
                  (self.total_messages, self.total_bytes))
            self.sock.close()

    def receive_data_streaming(self, client, resend):
        while True:
            try:
                data = client.recv(self.prefix_size)
                print(data)
                if data:
                    if resend:
                        self.client.send_partial_data(data)
                    self.total_messages += ONE
                    self.total_bytes += len(data)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

    def listen_to_client(self, client, address):
        print("Client connected")
        self.receive_data_streaming(client, self.is_client_too)




