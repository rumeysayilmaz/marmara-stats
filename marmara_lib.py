import platform
import os
import re
import slickrpc


""" 
String -> slickrpc.Proxy
creating proxy object for provided ac_name by searching for rpc credentials locally 
"""


def def_credentials(chain, mode="usual"):
    rpcport = ''
    ac_dir = ''
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Win64' or operating_system == 'Windows':
        ac_dir = '%s/komodo/' % os.environ['APPDATA']
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    if len(rpcport) == 0:
        if chain == 'KMD':
            rpcport = 7771
        else:
            print("rpcport not in conf file, exiting")
            print("check " + coin_config_file)
            exit(1)
    return slickrpc.Proxy("http://%s:%s@127.0.0.1:%d" % (rpcuser, rpcpassword, int(rpcport)))


"""
returns marmaraamountstat for provided MCL daemon proxy
"""


def marmara_amount_stat(marmara_proxy, begin_height, end_height):
    while True:
        try:
            marmara_amount_stat_info = marmara_proxy.marmaraamountstat(begin_height, end_height)
            return marmara_amount_stat_info
            break
        except Exception as e:
            print(e)
            print("Something went wrong. Please check your input")
            break


"""
stops the MCL daemon proxy
"""


def stop_chain(marmara_proxy):
    print("Stopping daemon")
    marmara_proxy.stop()


"""
gets the blocktime for a given height
"""


def get_block_time(marmara_proxy, height):
    try:
        block_time = marmara_proxy.getblock(height)['time']
    except Exception:
        raise Exception("Connection error!")
    return block_time
