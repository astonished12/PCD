import TCP.tcpServer as Server
import TCP.tcpClient as Client


IP_ADDRESS = "localhost"
PORT = 2002


def main():
    server = Server.ThreadedServerTCP(IP_ADDRESS, PORT, 2048)
    server.listen()


main()