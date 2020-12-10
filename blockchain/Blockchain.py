import json
from pprint import pprint

from redis import Redis

from blockchain.Block import Block
from blockchain.Transaction import Transaction
from utils.utils import get_config, get_logger

import logging


class Blockchain:
    def __init__(self):
        self.pending_transaction = []
        self.config = get_config()
        self.redis_client = Redis(host=self.config.redis.host,
                                  port=self.config.redis.port,
                                  db=self.config.redis.db,
                                  password=self.config.redis.password)
        self.difficulty = self.config.blockchain.difficulty
        self.mining_reward = self.config.blockchain.mining_reward
        self.redis_blockchain_key = "blockchain"
        self.logger = get_logger()

        self.create_genesis_block()

    def push_new_block(self, block):
        self.redis_client.lpush(self.redis_blockchain_key, json.dumps(vars(block)))

    def get_last_block(self):
        last_block = json.loads(self.redis_client.lindex(self.redis_blockchain_key, index=0))
        return Block.from_dict(last_block)

    def get_chain(self):
        res = []
        chain = self.redis_client.lrange(self.redis_blockchain_key, 0, -1)
        if chain:
            for block in chain[::-1]:
                res.append(Block.from_dict(json.loads(block)))

        return res

    def create_genesis_block(self):
        genesis_block = Block()
        genesis_block.hash = genesis_block.calculate_hash()
        if not self.get_chain():
            self.push_new_block(genesis_block)
        return genesis_block

    def get_all_transactions_for_wallet(self, address):
        txs = []
        chain = self.get_chain()
        for block in chain:
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
        block.index = len(self.get_chain())
        block.previous_hash = self.get_last_block().hash
        block.difficulty = self.difficulty
        block.mine_block(self.difficulty)

        self.logger.info(f"Block successfully mined: {vars(block)}")
        self.push_new_block(block)

        self.pending_transaction = []
        return block

    def add_transaction(self, transaction):
        if not transaction.from_address or not transaction.to_address:
            raise Exception("Transaction must have from and to address")

        if not transaction.is_valid():
            raise Exception("Cannot add invalid transaction")

        if not transaction:  # the amount of transactions is bigger than 0
            raise Exception("Transactions amount should be bigger than 0")

        # TODO uncomment
        # if self.get_address_balance(transaction.from_address) < transaction.amount:
        #     raise Exception("Not enought balance")

        self.pending_transaction.append(vars(transaction))
        self.logger.info(f"Transaction added: {vars(transaction)}")

    def get_address_balance(self, address):
        balance = 0
        chain = self.get_chain()
        for block in chain:
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
        chain = self.get_chain()  # TODO optimize return of all chain

        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            if not current_block.has_valid_transaction():
                self.logger.warning("Current block has invalid transaction")
                return False

            if current_block.hash != current_block.calculate_hash():
                self.logger.warning("Current block hash does not equals to real hash")
                return False

            if current_block.previous_hash != previous_block.hash:

                self.logger.warning("Previous block hash does not equal to current block's previous hash")
                self.logger.warning(current_block)
                self.logger.warning(previous_block)
                return False

        return True
