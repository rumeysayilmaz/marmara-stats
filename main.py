import time

import marmaradb
from marmara_lib import *

Height = 1
chain_name = "MCL"

rpc_connection = def_credentials(chain_name)
i = 0  # for test
while True:
    try:
        block = rpc_connection.getinfo()['blocks']
        stat_last_record = marmaradb.read_record('SELECT * FROM marmarastat ORDER BY height DESC LIMIT 1')
        last_record = stat_last_record[0]
        stat_last_record_connection = stat_last_record[1]
        stat_last_record_cursor = stat_last_record[2]
        print(last_record)
        if not last_record:  # if no record
            Height = 1
        elif last_record:
            Height = last_record[0][0] + 1  # last_record[0] bring the record , last_record[0][0] = Height in record
            print(Height)
        if Height <= (block - 3):
            BlockTime = get_block_time(rpc_connection, str(Height))
            stat_rpc_result = marmara_amount_stat(rpc_connection, str(Height), str(Height))
            TotalNormals = stat_rpc_result['TotalNormals']
            TotalActivated = stat_rpc_result['TotalActivated']
            TotalLockedInLoops = stat_rpc_result['TotalLockedInLoops']
            SpentNormals = stat_rpc_result['SpentNormals']
            SpentActivated = stat_rpc_result['SpentActivated']
            SpentLockedInLoops = stat_rpc_result['SpentLockedInLoops']
            if Height == 1:
                CalculatedTotalNormals = TotalNormals
                CalculatedTotalActivated = TotalActivated
                CalculatedTotalLockedInLoops = TotalLockedInLoops
                insert_marmara_stat_query = "INSERT INTO " \
                                                    "marmarastat(Height, TotalNormals, TotalActivated, TotalLockedInLoops, " \
                                                "SpentNormals, SpentActivated, SpentLockedInLoops, BlockTime, " \
                                                "CalculatedTotalNormals, CalculatedTotalActivated, CalculatedTotalLockedInLoops) " \
                                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                args = [Height, TotalNormals, TotalActivated, TotalLockedInLoops, SpentNormals, SpentActivated, SpentLockedInLoops,
                        BlockTime, CalculatedTotalNormals, CalculatedTotalActivated, CalculatedTotalLockedInLoops]
                insert_to_db = marmaradb.insert_record_set(insert_marmara_stat_query, args)
                marmaradb.close_connection(stat_last_record_connection, stat_last_record_cursor)
            if Height > 1:
                CalculatedTotalNormals = TotalNormals - SpentNormals + float(last_record[0][8])  # last_record[0][8] CalculatedTotalNormals from last record
                CalculatedTotalActivated = TotalActivated - SpentActivated + float(last_record[0][9])  # last_record[0][9] CalculatedTotalActivated from last record
                CalculatedTotalLockedInLoops = TotalLockedInLoops - SpentLockedInLoops + float(last_record[0][10])  # last_record[0][10] CalculatedTotalLockedInLoops from last record
                insert_marmara_stat_query = "INSERT INTO " \
                                            "marmarastat(Height, TotalNormals, TotalActivated, TotalLockedInLoops, " \
                                            "SpentNormals, SpentActivated, SpentLockedInLoops, BlockTime, " \
                                            "CalculatedTotalNormals, CalculatedTotalActivated, CalculatedTotalLockedInLoops) " \
                                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                args = [Height, TotalNormals, TotalActivated, TotalLockedInLoops, SpentNormals, SpentActivated,
                        SpentLockedInLoops,
                        BlockTime, CalculatedTotalNormals, CalculatedTotalActivated, CalculatedTotalLockedInLoops]
                insert_to_db = marmaradb.insert_record_set(insert_marmara_stat_query, args)
                marmaradb.close_connection(stat_last_record_connection, stat_last_record_cursor)
        if Height > (block-5):
            time.sleep(30)
        # test ----------
        i = i + 1
        if i == 500000:
            break
        # --------------
    except Exception as e:
        print(e)
        print("Daemon is not ready for RPC calls. Lets wait")
        time.sleep(10)
