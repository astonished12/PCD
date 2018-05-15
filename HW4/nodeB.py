import TCP.tcpServer as Server
import TCP.tcpClient as Client


IP_ADDRESS = "localhost"
PORT = 2000

IP_ADDRESS_TO_CONNECT = "34.217.75.237"
PORT_TO_CONNECT = 2001


def main():
    server = Server.ThreadedServerTCP(IP_ADDRESS, PORT, 2048, IP_ADDRESS_TO_CONNECT, PORT_TO_CONNECT)
    server.listen()


main()