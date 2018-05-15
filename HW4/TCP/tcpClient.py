import socket
import time



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

    def send_data_streaming(self, number_iter):
        total_messages = ZERO
        total_bytes = ZERO
        i = 0
        try:
            # Send data
            while i < number_iter:
                curr_time = time.time()
                bytess = bytes(str(curr_time)[0:16], 'utf-8')
                print(bytess)
                self.sock.send(bytess)
                total_messages += ONE
                i += 1
        except Exception as e:
            print(e)

        finally:
            return total_messages, total_bytes
            pass

    def send_partial_data(self, data_binary):
        print(data_binary)
        bytess = bytes(str(time.time())[0:16], 'utf-8')
        bytess += data_binary
        self.sock.send(bytess)



