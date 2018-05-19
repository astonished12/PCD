import TCP.tcpServer as Server
import TCP.config as Config
import DbManager.mysqlManager as DbManager


def main():
    node__d_logger = Config.make_logger("nodeD")

    db_manager = DbManager.MysqlManager()
    db_manager.create_tables()
    server = Server.ThreadedServerTCP(Config.localhost, Config.node_D_PORT, Config.packer_format_node_D, node__d_logger, conn_address=None,conn_port=None, db_manager=db_manager)
    server.listen()


main()