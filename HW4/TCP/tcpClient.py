import socket


# Create a TCP/IP socket

# Connect the socket to the port where the server is listening

#####
ZERO = 0
ONE = 1
####


class ClientTCP(object):
    def __init__(self, host, port, prefix_size):
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
                bytes_to_send = f.read(self.prefix_size)
                while bytes_to_send:
                    self.sock.send(bytes_to_send)
                    total_messages += ONE
                    total_bytes += len(bytes_to_send)
                    bytes_to_send = f.read(self.prefix_size)
        finally:
            return total_messages, total_bytes
            pass

    def send_partial_data(self, data_binary):
        self.sock.send(data_binary)



