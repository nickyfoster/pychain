from Block import Block
from Transaction import Transaction


class Blockchain:
    """
    A class representing a blockchain. A blockchain consists of a series of blocks,
    each containing a list of transactions. The blockchain also has a list of
    pending transactions that are waiting to be added to a block.

    Attributes:
        chain (list): A list of blocks in the blockchain.
        pending_transaction (list): A list of transactions that are waiting to be added to a block.
        difficulty (int): The difficulty level for mining new blocks.
        mining_reward (int): The reward given to miners for adding a block to the blockchain.

    """
    def __init__(self):
        self.chain = [self.__create_genesis_block()]
        self.pending_transaction = []
        self.difficulty = 2
        self.mining_reward = 100

    @staticmethod
    def __create_genesis_block() -> Block:
        """
        Create the first block in the blockchain (also known as the genesis block).

        Returns:
            Block: The genesis block.
        """
        genesis_block = Block()
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def __get_last_block(self) -> Block:
        """
        Get the last block in the blockchain.

        Returns:
            Block: The last block in the blockchain.
        """
        return self.chain[-1]

    def mine_pending_transaction(self, mining_reward_address: str) -> None:
        """
        Mine a new block containing the pending transactions and add it to the blockchain.

        Args:
            mining_reward_address (str): The address to receive the mining reward.
        """
        block = Block(transactions=self.pending_transaction)
        block.mine_block(self.difficulty)
        print(f"Block successfully mined!")
        self.chain.append(block)
        self.pending_transaction = [
            vars(Transaction(from_address="mining_reward_addr",
                             to_address=mining_reward_address,
                             amount=self.mining_reward))
        ]

    def create_transaction(self, transaction: Transaction) -> None:
        """
        Create a new transaction and add it to the list of pending transactions.

        Args:
            transaction (Transaction): The transaction to add.
        """
        self.pending_transaction.append(transaction.__dict__)

    def add_block(self, transactions=None) -> None:
        """
        Add a new block to the blockchain.

        Args:
            transactions (list, optional): A list of transactions to include in the block.
        """
        block = Block(transactions=transactions)
        block.previous_hash = self.__get_last_block().hash
        block.index = len(self.chain)
        block.mine_block(difficulty=self.difficulty)
        self.chain.append(block)

    def get_address_balance(self, address: str) -> int:
        """
        Get the balance for a given address by checking all transactions involving that address in the blockchain.

        Args:
            address (str): The address to check the balance for.

        Returns:
            int: The balance for the given address.
        """
        balance = 0
        for block in self.chain:
            if block.transactions:
                if len(block.transactions) > 0:
                    for transaction in block.transactions:
                        _transaction = Transaction.from_dict(transaction)
                        if _transaction.from_address == address:
                            balance -= _transaction.amount
                        if _transaction.to_address == address:
                            balance += _transaction.amount

        return balance

    def validate_chain(self) -> bool:
        """
        Validate the integrity of the blockchain by checking the hashes of all blocks and ensuring that they are all
        valid.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
