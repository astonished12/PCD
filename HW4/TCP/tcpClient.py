import socket
import time
import struct
import TCP.config as Config

# Create a TCP/IP socket

# Connect the socket to the port where the server is listening


class ClientTCP(object):
    def __init__(self, host, port, format_pack):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.sock.connect(self.server_address)
        self.format_pack = format_pack
        self.packer_rtt_obj = struct.Struct(Config.packer_rtt)
        self.packer_obj = struct.Struct(self.format_pack)
        self.rtt = self.compute_rtt()

    def send_tcp_packs(self, number_iter):
        self.send_rtt()
        i = 0
        try:
            # Send data
            while i < number_iter:
                print(i)
                curr_time = time.time()
                pack = self.packer_obj.pack(0, curr_time, self.server_address[0].encode("utf-8"))
                self.sock.send(pack)
                i += 1

        except Exception as e:
            print(e)

        finally:
            pass

    def compute_rtt(self):
        emit_time = time.time()
        pack = self.packer_rtt_obj.pack(1, emit_time, 0, 0)
        self.sock.send(pack)
        x = self.sock.recv(3).decode("utf-8")
        print("ACI ", x)
        receive_time = time.time()
        return receive_time-emit_time

    def send_rtt(self):
        pack = self.packer_rtt_obj.pack(2, self.rtt, 0, 0)
        self.sock.send(pack)

    def redirect_pack_data(self, pack):
        time_struct = struct.Struct(self.format_pack).unpack(pack)
        time_struct = list(time_struct)

        time_struct.append(time.time())
        time_struct.append(self.server_address[0].encode("utf-8"))
        pack = struct.Struct(self.format_pack+Config.packer_prefix).pack(*time_struct)
        self.sock.send(pack)

    def redirect_rtt(self, pack):
        rtt_struct = self.packer_rtt_obj.unpack(pack)
        rtt_struct = list(rtt_struct)
        j = 1
        while j < len(rtt_struct):
            if rtt_struct[j] == 0:
                rtt_struct[j] = self.rtt
                break
            j += 1

        pack = self.packer_rtt_obj.pack(*rtt_struct)
        self.sock.send(pack)




