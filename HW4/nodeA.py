import subprocess
import random
import TCP.tcpClient as Client


TMP_FILE_PATH = "./data.log"
MAX_FILE_SIZE = 100
MIN_FILE_SIZE = 5

IP_ADDRESS_TO_CONNECT = "54.213.227.231"
PORT = 2002

COMMAND = "dd if=/dev/urandom of=data.log bs=1M count='%d'"


def generate_tmp_data():
    size = random.randint(MIN_FILE_SIZE, MAX_FILE_SIZE)
    subprocess.call(COMMAND % size, shell=True)


def main():
    generate_tmp_data()
    client = Client.ClientTCP(IP_ADDRESS_TO_CONNECT, PORT, 2040)
    client.send_data_streaming(TMP_FILE_PATH)


main()