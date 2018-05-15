import TCP.tcpServer as Server
import TCP.tcpClient as Client


IP_ADDRESS = "localhost"
PORT = 2001

IP_ADDRESS_TO_CONNECT = "18.237.90.27"
PORT_TO_CONNECT = 2002


def main():
    server = Server.ThreadedServerTCP(IP_ADDRESS, PORT, 2048, IP_ADDRESS_TO_CONNECT, PORT_TO_CONNECT)
    server.listen()


main()