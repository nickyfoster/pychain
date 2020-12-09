from dataclasses import dataclass

from utils.utils import BaseDataclass, ChainUnit


@dataclass()
class Transaction(BaseDataclass, ChainUnit):
    from_address: str
    to_address: str
    amount: int

    def sign_transaction(self, signing_key):
        hash_tx = self.calculate_hash()
        sig = signing_key.sign(hash_tx, 'base64')