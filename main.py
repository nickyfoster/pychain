from Blockchain import Blockchain
from Transaction import Transaction

address_one = "0x1"
address_two = "0x2"

# Initialize Blockchain and first Transaction objects
blockchain = Blockchain()
transaction1 = Transaction(from_address=address_one, to_address=address_two, amount=50)

# Add our first transaction to blockchain.chain
blockchain.create_transaction(transaction1)

# Mine out first block and receive mining reward
blockchain.mine_pending_transaction(mining_reward_address=address_one)

print(blockchain.chain)


