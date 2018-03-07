import ClientProtocols.ClientTCP as ClientTcp
import ClientProtocols.ClientUDP as ClientUdp
import subprocess
import sys
import random
import time

######
TMP_FILE_PATH = "./data.log"
MAX_FILE_SIZE = 100
MIN_FILZE_SIZE = 5
ITERATIONS = 10


IP_ADDRESS = "localhost"
PORT = 2000
STREAMING_OPTION = "STREAM"
STOP_AND_WAIT_OPTION = "STOP"
TCP = "TCP"
UDP = "UDP"
COMMAND = "dd if=/dev/urandom of=data.log bs=1M count='%d'"

###

def generate_tmp_data():
    size = random.randint(MIN_FILZE_SIZE, MAX_FILE_SIZE)
    subprocess.call(COMMAND % size, shell=True)

def main():
    if len(sys.argv) < 4:
        print("Argument format wrong: UDP/TCP STREAM/TCP 0<x<65536")
  
    iter = 0
    if sys.argv[1] == TCP:
            client = ClientTcp.ClientTCP(IP_ADDRESS, PORT, int(sys.argv[3]))
    elif sys.argv[1] == UDP:
            client = ClientUdp.ClientUDP(IP_ADDRESS, PORT, int(sys.argv[3]))


    total_time = 0 
    total_mesages = 0
    total_bytes = 0
    
    while iter < ITERATIONS:
        generate_tmp_data()
        
        start_time = time.time()
        print("Current iteration is: ",iter)
        res = ()
        if sys.argv[2]==STREAMING_OPTION:
            res = client.send_data_streaming(TMP_FILE_PATH)
        elif sys.argv[2]==STOP_AND_WAIT_OPTION:
            res = client.send_data_stop_and_wait(TMP_FILE_PATH)
        total_mesages += res[0]
        total_bytes += res[1]
        elapsed_time = time.time() - start_time

        total_time+=elapsed_time

        iter += 1

    print("Total time = %f  ,total messages = %d total bytes = %d" %(total_time, total_mesages, total_bytes))

main()