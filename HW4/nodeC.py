import TCP.tcpServer as Server
import TCP.config as Config


def main():
    server = Server.ThreadedServerTCP(Config.localhost, Config.node_C_PORT, Config.padding_C, Config.node_D_IP_ADDRESS, Config.node_D_PORT)
    server.listen()


main()