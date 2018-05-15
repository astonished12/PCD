import TCP.tcpClient as Client
import TCP.config as Config


def main():
    client = Client.ClientTCP(Config.node_B_IP_ADDRESS, Config.node_B_PORT, Config.padding_B)
    client.send_data_streaming(10)


main()