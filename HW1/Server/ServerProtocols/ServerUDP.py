
import socketserver as SocketServer, threading, time

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        if self.server.mechanism=="STREAM":
            pass
            #print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
            self.server.total_messages += 1
            self.server.total_bytes += len(data)
        elif self.server.mechanism=="STOP":
            #print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
            self.server.total_messages += 1
            self.server.total_bytes += len(data)
            socket.sendto(bytes("ACK","utf-8"), self.client_address)

        

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
      pass  

def start(host,port,mechanism):

            server = ThreadedUDPServer((host, port), ThreadedUDPRequestHandler)
            server.mechanism = mechanism
            server.total_bytes = 0
            server.total_messages = 0
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