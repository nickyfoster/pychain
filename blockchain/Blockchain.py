from blockchain.Block import Block
from blockchain.Transaction import Transaction
from utils.utils import get_config


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transaction = []
        self.config = get_config()
        self.difficulty = self.config.blockchain.difficulty
        self.mining_reward = 100

    @staticmethod
    def create_genesis_block():
        genesis_block = Block()
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transaction(self, mining_reward_address):
        block = Block(transactions=self.pending_transaction)
        block.mine_block(self.difficulty)
        print(f"Block successfully mined!")
        self.chain.append(block)
        self.pending_transaction = [
            vars(Transaction(from_address="",
                             to_address=mining_reward_address,
                             amount=self.mining_reward))
        ]

    def create_transaction(self, transaction):
        self.pending_transaction.append(transaction.__dict__)

    def add_block(self, transactions=None):
        block = Block(transactions=transactions)
        block.previous_hash = self.get_last_block().hash
        block.index = len(self.chain)
        block.mine_block(difficulty=self.difficulty)
        self.chain.append(block)

    def get_address_balance(self, address):
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

    def validate_chain(self):
        # TODO add block index checking
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
