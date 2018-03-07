
import socketserver as SocketServer, threading, time

#####
ZERO = 0
ONE = 1 
ACK = "ACK"
TIME_OUT = 0.2
####


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        socket = self.request[1]
        current_thread = threading.current_thread()
        if self.server.mechanism=="STREAM":
               while True:
                    # Receive response
                #print('\nWaiting to receive..')
                try:
                    data, _ = socket.recvfrom(self.server.prefix_size)
                except Exception as err:
                    print(err)
                    continue
                if not data:
                    break
                else:
                    self.server.total_messages += 1
                    self.server.total_bytes += len(data)

        elif self.server.mechanism=="STOP":
            while True:
                # Receive response
                #print('\nWaiting to receive..')
                try:
                    data, _ = socket.recvfrom(self.server.prefix_size)
                except Exception as err:
                    print(err)
                    continue
                if not data:
                    break
                else:
                    self.server.total_messages += 1
                    self.server.total_bytes += len(data)
                    socket.sendto(bytes("ACK","utf-8"), self.client_address)

        

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
      pass  

def start(host,port,mechanism, prefix_size):

            server = ThreadedUDPServer((host, port), ThreadedUDPRequestHandler)
            server.mechanism = mechanism
            server.total_bytes = ZERO
            server.total_messages = ZERO
            server.prefix_size = prefix_size
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            try:
                server_thread.start()
                print("Server started at {} port {}".format(host, port))
                while True: time.sleep(100)
            except (KeyboardInterrupt, SystemExit):
                print("Protocol used: UDP, total messages received : %d, total bytes received: %d"%(server.total_messages, server.total_bytes))
                server.shutdown()
                server.server_close()
            exit()