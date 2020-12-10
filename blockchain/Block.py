import time
from dataclasses import dataclass

from blockchain.Transaction import Transaction
from utils.utils import BaseDataclass, ChainUnit


@dataclass()
class Block(BaseDataclass, ChainUnit):
    index: int = 0
    timestamp: float = time.time()
    transactions: list = None
    previous_hash: str = "0"
    hash: str = "0"
    nonce: int = 0
    difficulty: int = None

    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != "".join("0" for x in range(difficulty)):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def has_valid_transaction(self):
        for transaction in self.transactions:
            _transaction = Transaction.from_dict(transaction)

            if not _transaction.is_valid():
                return False

        return True
