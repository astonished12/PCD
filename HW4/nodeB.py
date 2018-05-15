import TCP.tcpServer as Server
import TCP.tcpClient as Client
import TCP.config as Config


def main():
    server = Server.ThreadedServerTCP(Config.localhost, Config.node_B_PORT, Config.padding_B, Config.node_C_IP_ADDRESS, Config.node_C_PORT)
    server.listen()


main()