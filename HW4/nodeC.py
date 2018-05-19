import TCP.tcpServer as Server
import TCP.config as Config


def main():
    node__c_logger = Config.make_logger("nodeC")
    server = Server.ThreadedServerTCP(Config.localhost, Config.node_C_PORT, Config.packer_format_node_C, node__c_logger, Config.node_D_IP_ADDRESS, Config.node_D_PORT)
    server.listen()


main()