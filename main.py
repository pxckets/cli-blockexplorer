from turtlecoin import TurtleCoind
import time
from datetime import datetime
import json
import sys
from os import system, name  
from time import sleep 

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


#main loop
while menu == "0":
    print("Copyright (c) 2019, The Oscillate devlopers")
    print("")
    print("|----------------Options--------------|")
    print("_______________________________________")
    print("(1). Block Explorer")
    print("(2). View live current block statistics")
    print("(3). View transaction data")
    print("(4). Exit")
    print("_______________________________________")

    menu = input("Enter selection: ")

    #blockexplorer
    while menu == "1":

        clear()

        # request blockheight from user
        custom_height = input("Enter {} Block Height: ".format(coin_ticker))
        custom_header = oscillated.get_block_header_by_height(int(custom_height))

        # load our Json
        custom_header_dump = json.dumps(custom_header)
        custom_header_loads = json.loads(custom_header_dump)
    
        # use the data from the JSON
        custom_block_height = custom_height
        custom_block_size = custom_header_loads['result']['block_header']['block_size']
        custom_block_hash = custom_header_loads['result']['block_header']['hash']
        custom_block_reward = custom_header_loads['result']['block_header']['reward']
        custom_block_tx_count = custom_header_loads['result']['block_header']['num_txes']
        custom_block_hashrate = round(custom_header_loads['result']['block_header']['difficulty'] / 60 / 1000, 2)
        custom_block_timestamp = custom_header_loads['result']['block_header']['timestamp']

        # convert timestamp to UTC
        timestamp = custom_block_timestamp
        block_date = datetime.fromtimestamp(timestamp)

        clear()

        # Block Explorer GUI, but its CLI
        print("")
        print("                        {} Block {} Info".format(coin_ticker, custom_block_height))
        print("_________________________________________________________________________________")
        print("[-------------------------------------------------------------------------------]")
        print("[         Size: {}kb".format(custom_block_size))
        print("[-------------------------------------------------------------------------------]")
        print("[         Hash: {}".format(custom_block_hash))
        print("[-------------------------------------------------------------------------------]")
        print("[         Reward: {} atomic units".format(custom_block_reward))
        print("[-------------------------------------------------------------------------------]")
        print("[         Transaction count: {}".format(custom_block_tx_count))
        print("[-------------------------------------------------------------------------------]")
        print("[         Net Hashrate: {} kH/s".format(custom_block_hashrate))
        print("[-------------------------------------------------------------------------------]")
        print("[         Date: {}".format(block_date))
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
            print("                         Latest {} Block Data ({})) Info".format(coin_ticker, last_block_height))
            print("                           Data refreshes every {} seconds".format(update_time))
            print("_________________________________________________________________________________")
            print("[-------------------------------------------------------------------------------]")
            print("[         Size: {} bytes".format(last_block_size))
            print("[-------------------------------------------------------------------------------]")
            print("[         Hash: {}".format(last_block_hash))
            print("[-------------------------------------------------------------------------------]")
            print("[         Reward: {} atomic units".format(last_block_reward))
            print("[-------------------------------------------------------------------------------]")
            print("[         Transaction count: {}".format(last_block_tx_count))
            print("[-------------------------------------------------------------------------------]")
            print("[         Net Hashrate: {} kH/s".format(last_block_hashrate))
            print("[-------------------------------------------------------------------------------]")
            print("_________________________________________________________________________________")
            
            #chill for however long the user said
            time.sleep(int(update_time))
            
            clear()

    while menu == "3":

        #user input
         txn_hash = input("Enter {} TXN hash: ".format(coin_ticker))

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
         print("Amount: {}".format(txn_amount))
         print("Fee: {}".format(txn_fee))
         print("Block: {}".format(txn_block))
         print("Size: {} bytes".format(txn_size))
         print("Size Percentage of block: {}%".format(txn_size_percentage))
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
