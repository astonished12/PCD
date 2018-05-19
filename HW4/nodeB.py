import TCP.tcpServer as Server
import TCP.config as Config
import logging


def main():
    node__b_logger = Config.make_logger("nodeB")
    server = Server.ThreadedServerTCP(Config.localhost, Config.node_B_PORT, Config.packer_format_node_B, node__b_logger, Config.node_C_IP_ADDRESS, Config.node_C_PORT)
    server.listen()


main()