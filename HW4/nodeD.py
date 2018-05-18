import TCP.tcpServer as Server
import TCP.config as Config


def main():
    server = Server.ThreadedServerTCP(Config.localhost, Config.node_D_PORT, Config.packer_format_node_D)
    server.listen()


main()