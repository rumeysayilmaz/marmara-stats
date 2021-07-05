import platform
import os
import re
import slickrpc
import shutil
import time
import threading
import math
import requests
import json

"""
slickrpc.Proxy -> List
returns list with marmaraactivated addresses for provided MCL daemon proxy
"""


def marmara_list_addresses(marmara_proxy):
    marmara_list_activated_addresses = marmara_proxy.marmaralistactivatedaddresses()["WalletActivatedAddresses"]
    marmara_addresses_list = []
    for entry in marmara_list_activated_addresses:
        marmara_addresses_list.append(entry["activatedaddress"])
    return marmara_addresses_list




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
slickrpc.Proxy -> List
returns list TotalNormals, TotalActivated, TotalLockedInLoops with marmaraamountstat for provided MCL daemon proxy
"""


def marmara_amount_stat(marmara_proxy, begin_height, end_height):
    while True:
        try:
            marmara_amount_stat_info = marmara_proxy.marmaraamountstat(begin_height, end_height)
            print(marmara_amount_stat_info)
            total_normals = marmara_amount_stat_info["TotalNormals"]
            total_activated = marmara_amount_stat_info["TotalActivated"]
            total_locked_in_loops = marmara_amount_stat_info["TotalLockedInLoops"]
            return total_normals, total_activated, total_locked_in_loops
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
