import time
import json
import sys
import urllib.request
import os
from os import system, name  
from datetime import datetime
from turtlecoin import TurtleCoind

menu = "0"

#Clear console function
def clear(): 
  
    if name == "nt": 
        _ = system("cls") 
    else: 
        _ = system("clear") 

#CONFIG
coin_ticker = "OSL"
coin_name = "Oscillate"
block_time = 60 #seconds
coin_github = "https://github.com/oscillate-coin"
website = "http://oscillate.me/"
exchange = "https://tradecx.io/markets/osldoge"
discord = "https://discord.gg/b5JzwWa"
twitter = "https://twitter.com/CoinOscillate"
telegram = "https://telegram" # I hate telegram
btt_ann = "https://bitcointalk.org/index.php?topic=5116182.0"
default_node_ip = "eu.osl.pubnodes.com"
rpc_port = 21246
version = "1.1.13"
menu = "0"

#pools
#if you want more/less pools, goto line 254 and figure it out yourself.
pool1 = "http://159.203.95.84:8245/stats" #official pool (pxckets)
pool2 = "http://74.130.176.161:8245/stats" #DuckTownCrypto (Dr. Greenthumb)
pool3 = "http://osc.line-pool.ru/stats" #Line Pool (mawr)

pool1_name = "Official Pool"
pool2_name = "DuckTown"
pool3_name = "Line Pool"

#ask user if they want to use a custom node
user_node_selection = input("Would you like to use a custom node? y/n: ")
if user_node_selection == "y":

    # Request node IP from user
    while True:
        try:
            print("Make sure the daemon you are requesting has the --enable-blockexplorer argument enabled.")
            rpc_host = input("Daemon IP: ")
            response = os.system("ping " + rpc_host)
            break
        except ConnectionError:
            print("Connection error to node. Using default.") #does this even work??
            rpc_host = default_node_ip

elif user_node_selection == "n":
    rpc_host = str(default_node_ip) 

else:
    print("Invalid input, using default node.")

daemon = TurtleCoind(rpc_host, rpc_port)

swap = False #set to true if your coin is doing a swap
swap_height = 400000 #ignore this if you arent doing a swap. If you are, set this to your swap height.

block_height = daemon.get_last_block_header()
block_height_dump = json.dumps(block_height)
block_height_loads = json.loads(block_height_dump)
block_height = block_height_loads["result"]["block_header"]["height"]
if block_height > swap_height:
    swap = False
    swap_height = 0

#main menu loop
while menu == "0":
    print("Copyright (c) 2019, The Oscillate developers") # on jah dont remove this
    print("")
    print(str(coin_ticker) + " Block Explorer v" + str(version))
    print("")
    print(website)
    if swap == True:
        print("SWAP AT BLOCK " +str(swap_height))
        print("Join our discord " + str(discord) + " for more details")
    print("""

|----------------Options----------------|
|_______________________________________|
|                                       |
|(1). Block Explorer                    |
|(2). View live current net statistics  |
|(3). View transaction data             |
|(4). View Pool Information             |
|(5). Node Checker                      |
|(6). Links                             |
|(7). Exit                              |
|_______________________________________|""")

    menu = input("Enter selection: ")

    #blockexplorer
    while menu == "1":

        clear()

        #Hash or Height?
        height_or_hash = input("Do you want to search for a block by height or by hash?: ")

        if height_or_hash == "height":
            # request blockheight from user
            block_height = input("Enter " + str(coin_ticker) + " Block Height: ")
            block_header = daemon.get_block_header_by_height(int(block_height))

            # load our Json for block height input
            block_header_dump = json.dumps(block_header)
            block_header_loads = json.loads(block_header_dump)
            
            # use the data from the JSON for height input
            block_size = block_header_loads["result"]["block_header"]["block_size"]
            block_hash = block_header_loads["result"]["block_header"]["hash"]
            block_reward = block_header_loads["result"]["block_header"]["reward"]
            block_tx_count = block_header_loads["result"]["block_header"]["num_txes"]
            block_hashrate = round(block_header_loads["result"]["block_header"]["difficulty"] / 60 / 1000, 2)
            block_timestamp = block_header_loads["result"]["block_header"]["timestamp"]

        else:
             #request hash from user
             user_block_hash = input(str(coin_ticker) + " Block hash to view: ")
             user_block_hash_data = daemon.get_block_header_by_hash(str(user_block_hash))

             # load our Json for bock hash input
             user_block_hash_data_dumps = json.dumps(user_block_hash_data)
             user_block_hash_data_loads = json.loads(user_block_hash_data_dumps)

             # use the data from the JSON for hash input
             block_height = user_block_hash_data_loads["result"]["block_header"]["height"]
             block_size = user_block_hash_data_loads["result"]["block_header"]["block_size"]
             block_hash = user_block_hash_data_loads["result"]["block_header"]["hash"]
             block_reward = user_block_hash_data_loads["result"]["block_header"]["reward"]
             block_tx_count = user_block_hash_data_loads["result"]["block_header"]["num_txes"]
             block_hashrate = round(user_block_hash_data_loads["result"]["block_header"]["difficulty"] / 60 / 1000, 2)
             block_timestamp = user_block_hash_data_loads["result"]["block_header"]["timestamp"]
             
        # convert timestamp to UTC
        timestamp = block_timestamp
        block_date = datetime.fromtimestamp(timestamp)

        clear()

        # Block Explorer GUI, but its CLI
        print("")
        print("                        " + str(coin_ticker) + " Block " + str(block_height) + " Info")
        print("______________________________________________________________________________________")
        print("[------------------------------------------------------------------------------------]")
        print("[         Size: " + str(block_size) + " bytes")
        print("[------------------------------------------------------------------------------------]")
        print("[         Hash: " + str(block_hash))
        print("[------------------------------------------------------------------------------------]")
        print("[         Reward: " + str(block_reward) + " atomic units")
        print("[------------------------------------------------------------------------------------]")
        print("[         Transaction count: " + str(block_tx_count))
        print("[------------------------------------------------------------------------------------]")
        print("[         Net Hashrate: " + str(block_hashrate) + "kh/s")
        print("[------------------------------------------------------------------------------------]")
        print("[         Date: " + str(block_date))
        print("[------------------------------------------------------------------------------------]")
        print("______________________________________________________________________________________")

        # yeet or skeet
        menu = input("Press 1 to check another block, 0 to go back to the menu: ")

        clear()

    #current network information
    while menu == "2":

        clear()

        #Request time interval
        print(str(block_time) + " seconds is the recommended amount of time")
        update_time = input("How often do you want to update the info? In seconds: ")

        #so the user doesnt crash their PC
        if update_time == "0":
            print("Update time cannot be zero, setting to 3.")
            update_time = "3"
    

        #loop this shit
        while True:
            #snag that block
            try:
                last_block = daemon.get_last_block_header()
            except(ConnectionError):
                print("Error connecting to daemon!")
                menu = 0

            #load that JSON stuff
            last_block_dump = json.dumps(last_block)
            last_block_loads = json.loads(last_block_dump)

            #then load this stuff
            last_block_height = last_block_loads["result"]["block_header"]["height"]
            last_block_size = last_block_loads["result"]["block_header"]["block_size"]
            last_block_hash = last_block_loads["result"]["block_header"]["hash"]
            last_block_reward = last_block_loads["result"]["block_header"]["reward"]
            last_block_tx_count = last_block_loads["result"]["block_header"]["num_txes"]
            last_block_hashrate = round(last_block_loads["result"]["block_header"]["difficulty"] / 60 / 1000000, 2)
            last_block_timestamp = last_block_loads["result"]["block_header"]["timestamp"]

            clear()

            #yeah. this looks cool
            print("")
            print("                         Latest " + str(coin_ticker) + " Block Data (" + str(last_block_height) + ") Info")
            print("                           Data refreshes every " + str(update_time) + " seconds")
            print("_________________________________________________________________________________")
            print("[-------------------------------------------------------------------------------]")
            print("[         Last Size: " + str(last_block_size) + " bytes")
            print("[-------------------------------------------------------------------------------]")
            print("[         Last Hash: " + str(last_block_hash))
            print("[-------------------------------------------------------------------------------]")
            print("[         Last Reward: " + str(last_block_reward) + " atomic units")
            print("[-------------------------------------------------------------------------------]")
            print("[         TXNS in last block: " + str(last_block_tx_count))
            print("[-------------------------------------------------------------------------------]")
            print("[         Network Hashrate: " + str(last_block_hashrate) + "Mh/s")
            print("[-------------------------------------------------------------------------------]")
            if swap == True:
                print("[                           [ SWAP IN " + str(swap_height - last_block_height) + " BLOCKS ]")
                print("")
                print("[      Join our discord (" + str(discord) + ") for details about this swap]")
                print("")
                print("[-------------------------------------------------------------------------------]")
            print("_________________________________________________________________________________")
            
            #chill for however long the user said
            try:
                time.sleep(int(update_time))
            except ValueError:
                print("Update time must be an integer.")
                print("Setting update time to 5 seconds...")
                time.sleep(5)
                update_time = (5)

            clear()

    while menu == "3":

        #user input
         txn_hash = input("Enter " + str(coin_ticker) + " TXN hash: ")

         # send that data to the daemon, and get the response back
         txn_hash_data = daemon.get_transaction(txn_hash)

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
         print("|-------Transaction Information----------")
         print("|")
         print("| Amount: " + str(txn_amount) + " atomic units")
         print("| Fee: " + str(txn_fee))
         print("| Block: " + str(txn_block))
         print("| Size: " + str(txn_size) + " bytes")
         print("| Size Percentage of block: " + str(txn_size_percentage) + "%")
         print("")

         menu = input("Press 3 to check another TXN, 0 to go back to the menu: ")
         clear()

    while menu == "4":

        pool_data_loaded = False

        print("Loading pool data.... please wait...")

        pool1_response = urllib.request.urlopen(pool1)
        print("Information received from " + pool1_name)
        #pool2_response = urllib.request.urlopen(pool2)
        #print("Information received from " + pool2_name)
        pool3_response = urllib.request.urlopen(pool3)
        print("Information received from " + pool3_name)

        print("Information Retrieved from all pool servers.")

        pool1_data = json.loads(pool1_response.read())
        #pool2_data = json.loads(pool2_response.read())
        pool3_data = json.loads(pool3_response.read())

        network_hashrate = round(pool1_data["network"]["difficulty"] / 60 / 1000)

        pool1_hashrate = pool1_data["pool"]["hashrate"] / 1000
        pool1_miners = pool1_data["pool"]["miners"]
        pool1_fee = pool1_data["config"]["fee"]

        #pool2_hashrate = pool2_data["pool"]["hashrate"] / 1000
        #pool2_miners = pool2_data["pool"]["miners"]
        #pool2_fee = pool2_data["config"]["fee"]

        pool3_hashrate = pool3_data["pool"]["hashrate"] / 1000
        pool3_miners = pool3_data["pool"]["miners"]
        pool3_fee = pool3_data["config"]["fee"]


        total_pool_hashrate = round(pool1_hashrate + pool3_hashrate)
        total_pool_miners = pool1_miners + pool3_miners
        avg_hash_per_miner = round(total_pool_hashrate / total_pool_miners)
        
        know_hashrate_percentage = round((100 / network_hashrate) * total_pool_hashrate)

        clear()

        print("")
        print("----" + pool1_name + "----")
        print("Hash rate: " + str(pool1_hashrate) + " kh/s")
        print("Miners: " + str(pool1_miners))
        print("Fee: " + str(pool1_fee) + "%")
        print("_______________________")
        print("")
       # print("----" + pool2_name + "----")
       # print("Hash rate: " + str(pool2_hashrate) + " kh/s")
       # print("Miners: " + str(pool2_miners))
      #  print("Fee: " + str(pool2_fee) + "%")
       # print("_______________________")
        print("")
        print("----" + pool3_name + "----")
        print("Hash rate: " + str(pool3_hashrate) + " kh/s")
        print("Miners: " + str(pool3_miners))
        print("Fee: " + str(pool3_fee) + "%")
        print("_______________________")
        print("")
        print("Network hashrate: " + str(network_hashrate) + " Kh/s")
        print("")
        print("Total known hashrate: " + str(total_pool_hashrate) + " Kh/s")
        print("")
        print("Total miners: " + str(total_pool_miners))
        print("")
        print("Avg Hash per miner: " + str(avg_hash_per_miner) + " Kh/s")
        print("")
        print("Percentage of hashrate known: " + str(know_hashrate_percentage) + "%")

        if know_hashrate_percentage > 100:
            print("The total known hashrate is only " + str(know_hashrate_percentage - 100) + "%" + " higher than the actual network hashrate due to pools being lucky. Not an attack.")
            print("Nothing to worry about frens!!")
        
        elif know_hashrate_percentage < 100:
            print("The unkown " + str(100 - know_hashrate_percentage) + "%" + " Can be caused by solo miners, private pools, or a difficulty spike.")

        print("")

        menu = input("Enter 0 to go back to the main menu: ")

        clear()

    while menu == "5":
        node_ip = input("Enter node IP: ")

        daemon = TurtleCoind(node_ip, rpc_port)
        matching_data = 0

        try:
            node_data = daemon.get_last_block_header()
            connection_failed = False
        except:
            print("Connection Failed. Make sure that the " + coin_ticker + " daemon is running on the specified IP.")
            connection_failed = True

        if connection_failed == False:

            node_data_dump = json.dumps(node_data)
            node_data_loads = json.loads(node_data_dump)

            last_block_height = node_data_loads["result"]["block_header"]["height"]
            last_block_size = node_data_loads["result"]["block_header"]["block_size"]
            last_block_hash = node_data_loads["result"]["block_header"]["hash"]
            last_block_reward = node_data_loads["result"]["block_header"]["reward"]

            print("Connection with node " + node_ip + "Established. Information received from node:")
            print("")
            print("Comparing data with an official node... Please wait...")

            official_daemon = TurtleCoind(default_node_ip, rpc_port)
            official_data = official_daemon.get_last_block_header()
            official_data_dump = json.dumps(official_data)
            official_data_loads = json.loads(official_data_dump)

            official_last_block_height = official_data_loads["result"]["block_header"]["height"]
            official_last_block_size = official_data_loads["result"]["block_header"]["block_size"]
            official_last_block_hash = official_data_loads["result"]["block_header"]["hash"]
            official_last_block_reward = official_data_loads["result"]["block_header"]["reward"]

            if official_last_block_height == last_block_height:
                print("Block height matches..")
                matching_data = matching_data + 1
            else:
                print("Block Height does not match!")

            if official_last_block_size == last_block_size:
                print("Block size matches..")
                matching_data = matching_data + 1
            else:
                print("Block Size does not match!")

            if official_last_block_hash == last_block_hash:
                print("Block hash matches..")
                matching_data = matching_data + 1
            else:
                print("Block hash does not match!")
            
            if official_last_block_size == last_block_size:
                print("Block size matches..")
                matching_data = matching_data + 1
            else:
                print("Block Size does not match!")

            if official_last_block_reward == last_block_reward:
                print("Block reward matches..")
                matching_data = matching_data + 1
            else:
                print("Block reward does not match!")

            if matching_data == 5:
                print("")
                print("All data matches up with the official node!")

            elif matching_data < 5:
                print("")
                print("Data does not match up with official node. This may be because the node " + node_ip + " is off-chain.")
            
            menu = str(input("Enter 0 to go back to main menu, or 5 to check another node: "))

        else:      
            menu = str(input("Error occurred, enter 0 to go back to main menu, or 5 to try again: "))

    while menu == "6":
        print("-----BlockExplorer GitHub-----")
        print("https://github.com/pxckets/cli-blockexplorer")
        print("________________")
        print("-----" + str(coin_name) + " Github----")
        print(coin_github)
        print("________________")
        print("")
        print("-----" + str(coin_name) + " Discord----")
        print(discord)
        print("________________")
        print("")
        print("-----" + str(coin_name) + " Website----")
        print(website)
        print("________________")
        print("")
        print("----" + str(coin_name) + " Exchange----")
        print(exchange)
        print("________________")
        print("")
        print("----" + str(coin_name) + " Twitter-----")
        print(twitter)
        print("________________")
        print("")
        print("----" + str(coin_name) + " Telegram-----")
        print(telegram)
        print("________________")
        print("")
        print("----" + str(coin_name) + " BTT ANN-----")
        print(btt_ann)
        print("________________")
        print("--Mining Pool List--")
        print("https://miningpoolstats.stream/" + str(coin_name))
        print("________________")

        menu = input("Enter 0 to go back to the main menu: ")

    # wow atleast recommend this to a friend.
    while menu == "7":
        print("")
        print("Have a good day :)")
        print("Window will automatically close in 5 seconds...")
        time.sleep(5)
        quit()
menu = 0