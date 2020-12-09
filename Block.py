import hashlib
import json
import time
from dataclasses import dataclass


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
