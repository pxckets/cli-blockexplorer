from turtlecoin import TurtleCoind
import time
from datetime import datetime
import json
import sys
from os import system, name  
from time import sleep 
  
#how2geek
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# Request node IP from user
while True:
    try:
        rpc_host = input('Daemon IP: ')
        break
    except ConnectionError:
         print("Connection error to node. Please try again.")

rpc_port = 11246
oscillated = TurtleCoind(rpc_host, rpc_port)
menu = "0"

#main loop
while menu == "0":
    print("Copyright (c) 2019, The Oscillate devlopers")
    print("")
    print("-------Options------")
    print("")
    print("(1). Block Explorer")
    print("(2). View live current block statistics")
    print("(3). Exit")

    menu = input("Enter selection: ")

    #blockexplorer
    while menu == "1":

        # request blockheight from user
        custom_height = input("Enter Block Height: ")
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

        # Block Explorer GUI, but its CLI
        print("")
        print("                         Block " + str(custom_block_height) + " Info")
        print("")
        print("[-------------------------------------------------------------------------------]")
        print("         Size: " + str(custom_block_size) + "kb")
        print("[-------------------------------------------------------------------------------]")
        print("         Hash: " + str(custom_block_hash))
        print("[-------------------------------------------------------------------------------]")
        print("         Reward: " + str(custom_block_reward) + " atomic units")
        print("[-------------------------------------------------------------------------------]")
        print("         Transaction count: " + str(custom_block_tx_count))
        print("[-------------------------------------------------------------------------------]")
        print("         Net Hashrate: " + str(custom_block_hashrate) + "kh/s")
        print("[-------------------------------------------------------------------------------]")
        print("         Date: " + str(block_date))
        print("[-------------------------------------------------------------------------------]")
        print("")

        # yeet or skeet
        menu = input("Press 1 to check another block, 0 to go back to the menu: ")

    #current block stuffs
    while menu == "2":

        #snag that user input
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

            #load da JSON stuff
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

            #this this thing again
            print("")
            print("                         Latest Block Data (" + str(last_block_height) + ") Info")
            print("                         Data refreshes every " + update_time + " seconds")
            print("")
            print("[-------------------------------------------------------------------------------]")
            print("         Size: " + str(last_block_size) + "kb")
            print("[-------------------------------------------------------------------------------]")
            print("         Hash: " + str(last_block_hash))
            print("[-------------------------------------------------------------------------------]")
            print("         Reward: " + str(last_block_reward) + " atomic units")
            print("[-------------------------------------------------------------------------------]")
            print("         Transaction count: " + str(last_block_tx_count))
            print("[-------------------------------------------------------------------------------]")
            print("         Net Hashrate: " + str(last_block_hashrate) + "kh/s")
            print("[-------------------------------------------------------------------------------]")
            print("")
            
            #chill for a minute
            time.sleep(int(update_time))
            
            clear()

    while menu == "3":
        print("")
        print("https://github.com/pxckets/cli-blockexplorer")
        print("Have a good day :)")
        print("Window will automatically close in 5 seconds...")
        time.sleep(5)
        quit()
menu = 0