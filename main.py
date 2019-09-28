from turtlecoin import TurtleCoind
import time
from time import sleep
from datetime import datetime
import json
import sys
from os import system, name  

default_node_ip = "159.203.95.84"

#ask user if they want to use a custom node
user_node_selection = input("Would you like to use a custom node? y/n: ")
if user_node_selection == "y":

    # Request node IP from user
    while True:
        try:
            rpc_host = input('Daemon IP: ')
            break
        except ConnectionError:
            print("Connection error to node. Please try again.")

else:
    rpc_host = str(default_node_ip) 


#
# COIN CONFIG
#  
rpc_port = 11246
oscillated = TurtleCoind(rpc_host, rpc_port)
coin_ticker = "OSL"
menu = "0"

#The clear function used in the latest block feature
def clear(): 
  
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 


#main menu loop
while menu == "0":
    print("Copyright (c) 2019, The Oscillate developers")
    print("")
    print(str(coin_ticker) + " Block Explorer")
    print("")
    print("|----------------Options----------------|")
    print("|_______________________________________|")
    print("|                                       |")
    print("|(1). Block Explorer                    |")
    print("|(2). View live current net statistics  |")
    print("|(3). View transaction data             |")
    print("|(4). Exit                              |")
    print("|_______________________________________|")

    menu = input("Enter selection: ")

    #blockexplorer
    while menu == "1":

        clear()

        # request blockheight from user
        block_height = input("Enter " + str(coin_ticker) + " Block Height: ")
        block_header = oscillated.get_block_header_by_height(int(block_height))

        # load our Json
        block_header_dump = json.dumps(block_header)
        block_header_loads = json.loads(block_header_dump)
    
        # use the data from the JSON
        block_size = block_header_loads['result']['block_header']['block_size']
        block_hash = block_header_loads['result']['block_header']['hash']
        block_reward = block_header_loads['result']['block_header']['reward']
        block_tx_count = block_header_loads['result']['block_header']['num_txes']
        block_hashrate = round(block_header_loads['result']['block_header']['difficulty'] / 60 / 1000, 2)
        block_timestamp = block_header_loads['result']['block_header']['timestamp']

        # convert timestamp to UTC
        timestamp = block_timestamp
        block_date = datetime.fromtimestamp(timestamp)

        clear()

        # Block Explorer GUI, but its CLI
        print("")
        print("                        " + str(coin_ticker) + " Block " + str(block_height) + " Info")
        print("_________________________________________________________________________________")
        print("[-------------------------------------------------------------------------------]")
        print("[         Size: " + str(block_size) + " bytes")
        print("[-------------------------------------------------------------------------------]")
        print("[         Hash: " + str(block_hash))
        print("[-------------------------------------------------------------------------------]")
        print("[         Reward: " + str(block_reward) + " atomic units")
        print("[-------------------------------------------------------------------------------]")
        print("[         Transaction count: " + str(block_tx_count))
        print("[-------------------------------------------------------------------------------]")
        print("[         Net Hashrate: " + str(block_hashrate) + "kh/s")
        print("[-------------------------------------------------------------------------------]")
        print("[         Date: " + str(block_date))
        print("[-------------------------------------------------------------------------------]")
        print("_________________________________________________________________________________")

        # yeet or skeet
        menu = input("Press 1 to check another block, 0 to go back to the menu: ")

        clear()

    #current block information
    while menu == "2":

        clear()

        #Request time interval
        update_time = input("How often do you want to update the info? In seconds: ")

        #so the user doesnt crash their PC
        if update_time == "0":
            print("Update time cannot be zero, setting to 1.")
            update_time = "1"
    
        #loop this shit
        while True:
            #snag that block
            try:
                last_block = oscillated.get_last_block_header()
            except(ConnectionError):
                print("Error connecting to daemon!")
                menu = 0

            #load that JSON stuff
            last_block_dump = json.dumps(last_block)
            last_block_loads = json.loads(last_block_dump)

            #then load this stuff
            last_block_height = last_block_loads['result']['block_header']['height']
            last_block_size = last_block_loads['result']['block_header']['block_size']
            last_block_hash = last_block_loads['result']['block_header']['hash']
            last_block_reward = last_block_loads['result']['block_header']['reward']
            last_block_tx_count = last_block_loads['result']['block_header']['num_txes']
            last_block_hashrate = round(last_block_loads['result']['block_header']['difficulty'] / 60 / 1000, 2)
            last_block_timestamp = last_block_loads['result']['block_header']['timestamp']

            clear()

            #yeah. this looks cool
            print("")
            print("                         Latest " + str(coin_ticker) + " Block Data (" + str(last_block_height) + ") Info")
            print("                           Data refreshes every " + update_time + " seconds")
            print("_________________________________________________________________________________")
            print("[-------------------------------------------------------------------------------]")
            print("[         Size: " + str(last_block_size) + " bytes")
            print("[-------------------------------------------------------------------------------]")
            print("[         Hash: " + str(last_block_hash))
            print("[-------------------------------------------------------------------------------]")
            print("[         Reward: " + str(last_block_reward) + " atomic units")
            print("[-------------------------------------------------------------------------------]")
            print("[         Transaction count: " + str(last_block_tx_count))
            print("[-------------------------------------------------------------------------------]")
            print("[         Net Hashrate: " + str(last_block_hashrate) + "kh/s")
            print("[-------------------------------------------------------------------------------]")
            print("_________________________________________________________________________________")
            
            #chill for however long the user said
            time.sleep(int(update_time))
            
            clear()

    while menu == "3":

        #user input
         txn_hash = input("Enter " + str(coin_ticker) + " TXN hash: ")

         # send that data to the daemon, and get the response back
         txn_hash_data = oscillated.get_transaction(txn_hash)

        #JSON load
         txn_hash_dump = json.dumps(txn_hash_data)
         txn_hash_loads = json.loads(txn_hash_dump)

        #Information harvest
         txn_amount = txn_hash_loads["result"]["txDetails"]["amount_out"]
         txn_fee = txn_hash_loads["result"]["txDetails"]["fee"]
         txn_block = txn_hash_loads["result"]["block"]["height"]
         txn_size = txn_hash_loads["result"]["txDetails"]["size"]
         txn_size_percentage = round(100 / txn_hash_loads["result"]["block"]["cumul_size"] * txn_size)

        #TXN info gui but cli, you feel?
         print("")
         print("--------Transaction Information----------")
         print("")
         print("Amount: " + str(txn_amount) + " atomic units")
         print("Fee: " + str(txn_fee))
         print("Block: " + str(txn_block))
         print("Size: " + str(txn_size) + " bytes")
         print("Size Percentage of block: " + str(txn_size_percentage) + "%")
         print("")

         menu = input("Press 3 to check another TXN, 0 to go back to the menu: ")
         clear()

    # wow atleast recommend this to a friend.
    while menu == "4":
        print("")
        print("https://github.com/pxckets/cli-blockexplorer")
        print("Have a good day :)")
        print("Window will automatically close in 5 seconds...")
        time.sleep(5)
        quit()
menu = 0