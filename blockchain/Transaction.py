from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from dataclasses import dataclass

from utils.utils import BaseDataclass, ChainUnit, hex2bytes


@dataclass()
class Transaction(BaseDataclass, ChainUnit):
    from_address: str
    to_address: str
    amount: int
    signature: str = None

    def sign_transaction(self, signing_key):
        if signing_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                 format=serialization.PublicFormat.Raw).hex() != self.from_address:
            raise Exception("You cannot sign transaction for other wallets")

        self.signature = signing_key.sign(self.calculate_hash().encode()).hex()

    def is_valid(self):
        if not self.from_address:
            return True

        if not self.signature or len(self.signature) == 0:
            raise Exception("No signature in this transaction")

        public_key = ed25519.Ed25519PublicKey.from_public_bytes(hex2bytes(self.from_address))
        try:
            public_key.verify(signature=hex2bytes(self.signature),
                              data=self.calculate_hash().encode())
            return True
        except InvalidSignature:
            return False


if __name__ == '__main__':

    private_key = ed25519.Ed25519PrivateKey.generate()
    address = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                    format=serialization.PublicFormat.Raw).hex()

    transaction = Transaction(amount=10, from_address=address,
                              to_address="")
    transaction.sign_transaction(private_key)
    print(f"Is transaction valid: {transaction.is_valid()}")
