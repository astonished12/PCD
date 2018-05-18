import TCP.tcpClient as Client
import TCP.config as Config


def main():
    client = Client.ClientTCP(Config.localhost, Config.node_B_PORT, Config.packer_format_node_B)
    client.send_tcp_packs(10)


main()