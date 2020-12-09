import hashlib
import inspect
import json
import time
from dataclasses import dataclass


@dataclass()
class Payload:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_dict(cls, d):
        return cls(**{
            k: v for k, v in d.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass()
class Block:
    index: int = 0
    timestamp: float = time.time()
    transactions: list = None
    previous_hash: str = "0"
    hash: str = "0"
    nonce: int = 0

    def calculate_hash(self):
        return hashlib.sha256(json.dumps(self.__get_dict_from_block(), sort_keys=True).encode()).hexdigest()

    def __get_dict_from_block(self):
        _excluded_keys = ["hash"]  # We exclude `hash` key when calculating block's hash
        return dict(
            (key, value)
            for (key, value) in self.__dict__.items()
            if key not in _excluded_keys
        )

    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != "".join("0" for x in range(difficulty)):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block mined: {self.hash}")


@dataclass()
class Transaction(Payload):
    from_address: str
    to_address: str
    amount: int


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transaction = []
        self.difficulty = 2
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
            vars(Transaction(from_address="mining_reward_addr",
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
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
