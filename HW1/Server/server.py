import ServerProtocols.ServerTCP as ServerTcp
import ServerProtocols.ServerUDP as ServerUdp
import sys


def main():
    if len(sys.argv) < 4 or not (int(sys.argv[3]) > 0 and int(sys.argv[3])<65536):
        print("Argument format wrong: UDP/TCP STREAM/TCP 0<x<65536")
        exit()
    if sys.argv[1]=="TCP":
        if sys.argv[2]=="STREAM" or sys.argv[2]=="STOP":
               ServerTcp.ThreadedServerTCP('',2000,sys.argv[2], int(sys.argv[3])).listen()

    if sys.argv[1]=="UDP":
        if sys.argv[2]=="STREAM" or sys.argv[2]=="STOP":
               ServerUdp.start('',2000,sys.argv[2])

main()

