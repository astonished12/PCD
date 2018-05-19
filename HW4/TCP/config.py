import logging

localhost= "0.0.0.0"

node_A_IP_ADDRESS = "54.191.77.84"
node_A_PORT = 1999

node_B_IP_ADDRESS = "52.10.231.180"
node_B_PORT = 2000

node_C_IP_ADDRESS = "34.218.249.115"
node_C_PORT = 2001

node_D_IP_ADDRESS = "35.166.206.73"
node_D_PORT = 2002

packer_format_node_B = "!i d 12s"
packer_format_node_C = "!i d 12s d 12s"
packer_format_node_D = "!i d 12s d 12s d 12s"
packer_prefix = " d 12s"
packer_rtt = "!i d d d"

host_db_instance = 'mydbinstance.c1adwgxy7qm4.us-west-2.rds.amazonaws.com'
host_db_user = "astonished"
host_db_password = "Numlock123"
host_db_name = "TrafficNetworkDatabase"


def make_logger(node):
    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('logs/'+node+'.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger
