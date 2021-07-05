import marmaradb
from marmara_lib import *

BEGIN_HEIGHT = 1
chain_name = "MCL"

rpc_connection = def_credentials(chain_name)

while True:
    try:
        print(rpc_connection.getinfo())

        block = rpc_connection.getinfo()['blocks']
        stat_last_record = marmaradb.read_record('SELECT * FROM marmarastat ORDER BY id DESC LIMIT 1')
        print(block)
        print(stat_last_record[0])
        stat_last_record_id = stat_last_record[0]
        stat_last_record_connection = stat_last_record[1]
        stat_last_record_cursor = stat_last_record[2]
        print(stat_last_record[1])
        if not stat_last_record_id == []:
            last_id = stat_last_record_id[0][0]
            print(last_id)
            BEGIN_HEIGHT = last_id + 1
            print(BEGIN_HEIGHT)
        if BEGIN_HEIGHT <= (block - 5):
            BeginHeight = BEGIN_HEIGHT
            EndHeight = BEGIN_HEIGHT + 1
            stat_rpc_result = marmara_amount_stat(rpc_connection, str(BeginHeight), str(EndHeight))
            TotalNormals = stat_rpc_result['TotalNormals']
            TotalActivated = stat_rpc_result['TotalActivated']
            TotalLockedInLoops = stat_rpc_result['TotalLockedInLoops']
            insert_marmara_stat_query = "INSERT INTO " \
                                        "marmarastat(BeginHeight, EndHeight, TotalNormals, " \
                                        "TotalActivated, TotalLockedInLoops) " \
                                        "VALUES (%s, %s, %s, %s, %s)"

            args = [BeginHeight, EndHeight, TotalNormals, TotalActivated, TotalLockedInLoops]
            insert_to_db = marmaradb.insert_record_set(insert_marmara_stat_query, args)
            marmaradb.close_connection(stat_last_record_connection, stat_last_record_cursor)

        break
    except Exception as e:
        print(e)
        print("Daemon is not ready for RPC calls. Lets wait")
        time.sleep(10)
    # else:
    #     print("Successfully connected!\n")
    #     break

# try:
#     db_connection = mysql.connector.connect(
#         host="localhost",
#         user="admin",
#         password="****",
#         database="marmara",
#     )
#     show_table_query = "SHOW TABLES"
#     execute_sql(db_connection, show_table_query)
#
#     insert_marmara_stat_query = """
#          INSERT INTO marmarastat
#          (BeginHeight, EndHeight, TotalNormals, TotalActivated, TotalLockedInLoops)
#          VALUES (%s, %s, %s, %s, %s, %s)
#          """
#     marmara_stat_records = [(1, 2, 0, 0, 0)]
#     execute_sql_records(db_connection, insert_marmara_stat_query, marmara_stat_records)
#
#
# except Error as e:
#     print(e)

# if __name__ == '__main__':
# show_table_query = 'SHOW TABLES'
# marmaradb.execute_sql(show_table_query)

# x = conf_dir.stdout
# print(x)
# print('------------------------------------------')
# # conf_dir = os.environ['HOME']
# db_config_file = str(x) + '/db.conf'
# print(db_config_file)
#     insert_marmara_stat_query = """
#     INSERT INTO marmarastat
#     (BeginHeight, EndHeight, TotalNormals, TotalActivated, TotalLockedInLoops)
#     VALUES ( %s, %s, %s, %s, %s)
#     """
#     marmara_stat_records = [(1, 2, 0, 0, 0)]
