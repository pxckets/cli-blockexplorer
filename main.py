from turtlecoin import TurtleCoind
import json

rpc_host = 'localhost'
rpc_port = 11246
oscillated = TurtleCoind(rpc_host, rpc_port)
restart = "y"
while restart == "y":
    custom_height = input("What block do you want to view the info of?: ")
    custom_header = oscillated.get_block_header_by_height(int(custom_height))

    custom_header_dump = json.dumps(custom_header)
    custom_header_loads = json.loads(custom_header_dump)
 
    custom_block_height = custom_height
    custom_block_size = custom_header_loads['result']['block_header']['block_size']
    custom_block_hash = custom_header_loads['result']['block_header']['hash']
    custom_block_reward = custom_header_loads['result']['block_header']['reward']
    custom_block_tx_count = custom_header_loads['result']['block_header']['num_txes']

    print("")
    print("Block " + str(custom_block_height) + " Info")
    print("")
    print("Size: " + str(custom_block_size) + "kb")
    print("Hash: " + str(custom_block_hash))
    print("Reward: " + str(custom_block_reward) + " atomic units")
    print("Transaction count: " + str(custom_block_tx_count))

    restart = input("Do you want to check another block? y/n: ")
    

    

