import TCP.tcpServer as Server
import TCP.config as Config


def main():
    server = Server.ThreadedServerTCP(Config.localhost, Config.node_B_PORT, Config.packer_format_node_B, Config.localhost, Config.node_C_PORT)
    server.listen()


main()