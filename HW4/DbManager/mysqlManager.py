import pymysql
import TCP.config as Config


class MysqlManager(object):

    def __init__(self):
        self.connection = pymysql.connect(host=Config.host_db_instance,
                                     user=Config.host_db_user,
                                     password=Config.host_db_password,
                                     db=Config.host_db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        self.create_table_delays = """CREATE TABLE `delays` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `sourceIP` varchar(21) COLLATE utf8_bin NOT NULL,
                `destinationIP` varchar(21) COLLATE utf8_bin NOT NULL,
                `hop1` varchar(100) COLLATE utf8_bin,
                `hop2` varchar(100) COLLATE utf8_bin,
                `hop3` varchar(100) COLLATE utf8_bin,
                `total_delay` varchar(100) COLLATE utf8_bin,
                PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
            AUTO_INCREMENT=1 ;
        """

        self.create_table_rtts = """CREATE TABLE `rtts` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `first_node->second_node` varchar(21) COLLATE utf8_bin NOT NULL,
            `second_node->third_node` varchar(21) COLLATE utf8_bin NOT NULL,
            `third_node->forth_node` varchar(21) COLLATE utf8_bin NOT NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
        AUTO_INCREMENT=1 ;
        """

        self.insert_data_into_delays_table_sql_command = """     
           INSERT INTO `delays` (`sourceIP`, `destinationIP`, `hop1`, `hop2`, `hop3`, `total_delay`) VALUES (%s, %s, %s, %s, %s, %s)
        """

        self.insert_data_into_rtts_table_sql_command = """
            INSERT INTO `rtts` (`first_node->second_node`, `second_node->third_node`, `third_node->forth_node`) VALUES (%s, %s, %s)            
        """

    def create_tables(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = self.create_table_delays
                sql1 = self.create_table_rtts
                cursor.execute(sql)
                cursor.execute(sql1)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            pass

    def insert_data_into_delays_table(self, source_ip, destination_ip, hop1, hop2, hop3, total_delay):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = self.insert_data_into_delays_table_sql_command
                cursor.execute(sql, (source_ip, destination_ip, hop1, hop2, hop3, total_delay))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            pass

    def insert_data_into_rtts_table(self, rtt_value_1, rtt_value_2, rtt_value_3):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = self.insert_data_into_rtts_table_sql_command
                cursor.execute(sql, (rtt_value_1, rtt_value_2, rtt_value_3))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            pass

