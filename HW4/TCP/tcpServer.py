import socket
import threading
import time
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
        print("Voi primi cate ", self.prefix_size)
        while True:
            try:
                data = client.recv(self.prefix_size)
                if data:
                    if resend:
                        self.client.send_partial_data(data)
                    else:
                        data = data[0:48].decode("utf-8")
                        current_time = time.time()

                        time_c_start_send_to_d_start = data[0:16]
                        time_elapsed_from_c_to_d = current_time-float(time_c_start_send_to_d_start)

                        time_b_start_send_to_c = data[16:32]
                        time_elapsed_from_b_to_c = float(time_c_start_send_to_d_start)-float(time_b_start_send_to_c)

                        time_a_send_to_b = data[32:48]
                        time_elapsed_from_a_to_b = float(time_b_start_send_to_c)-float(time_a_send_to_b)
                        print(str(time_elapsed_from_c_to_d)+" "+str(time_elapsed_from_b_to_c)+" "+str(time_elapsed_from_a_to_b))

                        self.total_messages += ONE
                        self.total_bytes += len(data)

            except Exception as e:
                print(e)
                client.close()
                return False

    def listen_to_client(self, client, address):
        print("Client connected")
        self.receive_data_streaming(client, self.is_client_too)




