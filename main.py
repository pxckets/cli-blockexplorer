from turtlecoin import TurtleCoind
import time
from datetime import datetime
import json

# Request node IP from user
while True:
    try:
        rpc_host = input('Daemon IP: ')
        break
    except ConnectionError:
         print("Connection error to node. Please try again.")

rpc_port = 11246
oscillated = TurtleCoind(rpc_host, rpc_port)

#blockexplorer
restart = "y"
while restart == "y":

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

    # GUI
    print("")
    print("                                Block " + str(custom_block_height) + " Info")
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
    restart = input("Do you want to check another block? y/n: ")
print('')
print("https://github.com/pxckets/cli-blockexplorer")
print("https://discord.gg/RsQDrhJ")
time.sleep(10)