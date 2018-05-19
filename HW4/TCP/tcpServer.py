import socket
import threading
import struct
import time
import TCP.tcpClient as Client
import TCP.config as Config

#####
ZERO = 0
ONE = 1
####


class ThreadedServerTCP(object):

    def __init__(self, host, port, format_pack, logger, conn_address=None, conn_port=None, db_manager=None):
        self.host = host
        self.port = port
        self.format_pack = format_pack
        self.logger = logger
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ONE)
        self.sock.bind((self.host, self.port))

        self.is_client_too = False
        if conn_address is not None and conn_port is not None:
            self.is_client_too = True
            self.client = Client.ClientTCP(conn_address, conn_port, self.format_pack)
        if db_manager is not None:
            self.db_manager = db_manager
            self.rtt_values = []
            self.delays_values = []

    def listen(self):
        self.sock.listen(5)
        try:
            while True:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target=self.listen_to_client, args=(client, address)).start()
        except (KeyboardInterrupt, SystemExit):
            self.sock.close()

    def analyzer_network_traffic(self, client, resend):
        print("Format packul este ", self.format_pack)
        packer_tcp_packs = struct.Struct(self.format_pack)
        packer_tcp_rtt = struct.Struct(Config.packer_rtt)
        while True:
            try:
                pack = client.recv(packer_tcp_rtt.size)
                if pack:
                    data = packer_tcp_rtt.unpack(pack)
                    data = list(data)

                    if data[0] == 1:
                        client.send(bytes("ACK", "utf-8"))
                        break
            except Exception as e:
                print(e)
                client.close()
                return False
        i = 0
        while i < 4:
            try:
                pack = client.recv(packer_tcp_rtt.size)
                if pack:
                    data = packer_tcp_rtt.unpack(pack)
                    data = list(data)

                if data[0] == 2:
                    if resend:
                        self.client.redirect_rtt(pack)
                        break
                    else:
                        receive_rtt_values_row = list()
                        print("rtt :"+str(data[1]) + " "+str(data[2])+" "+str(data[3]))
                        receive_rtt_values_row.append(str(data[1]))
                        receive_rtt_values_row.append(str(data[2]))
                        receive_rtt_values_row.append(str(data[3]))
                        self.rtt_values.append(receive_rtt_values_row)

                        break

            except Exception as e:
                print(e)
                client.close()
                return False

        while True:
            try:
                pack = client.recv(packer_tcp_packs.size)
                if pack:
                    data = packer_tcp_packs.unpack(pack)
                    data = list(data)

                    if data[0] == 3: #stop receive packets
                        if resend:
                            self.client.redirect_pack_data(pack)
                        else:
                            break

                    if data[0] == 0:
                        if resend:
                            self.client.redirect_pack_data(pack)
                        else:
                            ip_address__a = data[2].decode("utf-8").rstrip("\x00")
                            ip_address__b = data[4].decode("utf-8").rstrip("\x00")
                            ip_address__c = data[6].decode("utf-8").rstrip("\x00")
                            ip_address__d = self.host

                            current_time = time.time()

                            time_c_start_send_to_d_start = data[5]
                            time_elapsed_from_c_to_d = current_time-float(time_c_start_send_to_d_start)

                            time_b_start_send_to_c = data[3]
                            time_elapsed_from_b_to_c = float(time_c_start_send_to_d_start)-float(time_b_start_send_to_c)

                            time_a_send_to_b = data[1]
                            time_elapsed_from_a_to_b = float(time_b_start_send_to_c)-float(time_a_send_to_b)

                            total = time_elapsed_from_a_to_b+time_elapsed_from_b_to_c+time_elapsed_from_c_to_d

                            print(ip_address__a+" "+ip_address__d+" "+str(time_elapsed_from_a_to_b)+" "+str(time_elapsed_from_b_to_c)+" "+str(time_elapsed_from_c_to_d))

                            receive_delays_values_row = list()
                            receive_delays_values_row.append(ip_address__a)
                            receive_delays_values_row.append(ip_address__b)
                            receive_delays_values_row.append(str(time_elapsed_from_a_to_b))
                            receive_delays_values_row.append(str(time_elapsed_from_b_to_c))
                            receive_delays_values_row.append(str(time_elapsed_from_c_to_d))
                            receive_delays_values_row.append(str(total))

                            self.delays_values.append(receive_delays_values_row)
            except Exception as e:
                print(e)
                client.close()
                return False

        print("GO AND INSERT")
        for row in self.rtt_values:
            self.db_manager.insert_data_into_rtts_table(row[0], row[1], row[2])

        for row in self.delays_values:
            self.db_manager.insert_data_into_delays_table(row[0], row[1], row[2], row[3], row[4], row[5])

    def listen_to_client(self, client, address):
        print("Client connected")
        self.analyzer_network_traffic(client, self.is_client_too)




