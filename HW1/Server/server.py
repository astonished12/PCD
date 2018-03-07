import ServerProtocols.ServerTCP as ServerTcp
import ServerProtocols.ServerUDP as ServerUdp
import sys


#####
IP_ADDRESS = "localhost"
PORT = 2000

STREAMING_OPTION = "STREAM"
STOP_AND_WAIT_OPTION = "STOP"
TCP = "TCP"
UDP = "UDP"
#####

def main():
    if len(sys.argv) < 4 or not (int(sys.argv[3]) > 0 and int(sys.argv[3])<65536):
        print("Argument format wrong: UDP/TCP STREAM/STOP 0<x<65536")
        exit()
    if sys.argv[1]==TCP:
        if sys.argv[2]==STREAMING_OPTION or sys.argv[2]==STOP_AND_WAIT_OPTION:
               ServerTcp.ThreadedServerTCP(IP_ADDRESS, PORT, sys.argv[2], int(sys.argv[3])).listen()

    if sys.argv[1]==UDP:
        if sys.argv[2]==STREAMING_OPTION or sys.argv[2]==STOP_AND_WAIT_OPTION:
               ServerUdp.start(IP_ADDRESS, PORT, sys.argv[2], int(sys.argv[3]))

main()

