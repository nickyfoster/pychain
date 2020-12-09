import time
from dataclasses import dataclass

from utils.utils import BaseDataclass, ChainUnit


@dataclass()
class Block(BaseDataclass, ChainUnit):
    index: int = 0
    timestamp: float = time.time()
    transactions: list = None
    previous_hash: str = "0"
    hash: str = "0"
    nonce: int = 0

    def mine_block(self, difficulty):
        while self.hash[0:difficulty] != "".join("0" for x in range(difficulty)):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block mined: {self.hash}")
