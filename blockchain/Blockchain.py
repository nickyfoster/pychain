from blockchain.Block import Block
from blockchain.Transaction import Transaction
from utils.utils import get_config


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transaction = []
        self.config = get_config()
        self.difficulty = self.config.blockchain.difficulty
        self.mining_reward = self.config.blockchain.mining_reward

    @staticmethod
    def create_genesis_block():
        genesis_block = Block()
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def get_last_block(self):
        return self.chain[-1]

    def get_all_transactions_for_wallet(self, address):
        txs = []
        for block in self.chain:
            if block.transactions:
                for tx in block.transactions:
                    if tx:
                        _tx = Transaction.from_dict(tx)
                        if _tx.from_address == address or _tx.to_address == address:
                            txs.append(tx)

        return txs

    def mine_pending_transaction(self, mining_reward_address):
        reward_tx = Transaction(None, mining_reward_address, self.mining_reward)
        self.pending_transaction.append(vars(reward_tx))

        block = Block(transactions=self.pending_transaction)
        block.index = len(self.chain)
        block.previous_hash = self.get_last_block().hash
        block.mine_block(self.difficulty)

        print(f"Block successfully mined!")
        self.chain.append(block)

        self.pending_transaction = []

    def add_transaction(self, transaction):
        if not transaction.from_address or not transaction.to_address:
            raise Exception("Transaction must have from and to address")

        if not transaction.is_valid():
            raise Exception("Cannot add invalid transaction")

        if not transaction:  # the amount of transactions is bigger than 0
            raise Exception("Transactions amount should be bigger than 0")

        # if self.get_address_balance(transaction.from_address) < transaction.amount:
        #     raise Exception("Not enought balance")

        self.pending_transaction.append(vars(transaction))
        print(f"Transaction added: {vars(transaction)}")

    def get_address_balance(self, address):
        balance = 0
        for block in self.chain:
            if block.transactions:
                if len(block.transactions) > 0:
                    # TODO check for negative amount of money
                    for transaction in block.transactions:
                        _transaction = Transaction.from_dict(transaction)
                        if _transaction.from_address == address:
                            balance -= _transaction.amount
                        if _transaction.to_address == address:
                            balance += _transaction.amount

        return balance

    def validate_chain(self):
        # TODO add block index checking
        if vars(self.create_genesis_block()) != vars(self.chain[0]):
            return False

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if not current_block.has_valid_transaction():
                return False

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
