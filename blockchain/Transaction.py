import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from dataclasses import dataclass

from utils.utils import BaseDataclass, ChainUnit, hex2bytes

# TODO lookup how Bitcoin generates wallter address
# https://medium.com/@tunatore/how-to-generate-bitcoin-addresses-technical-address-generation-explanation-and-online-course-a6b46a2fe866
# TODO add sender_public_key to transaction
# and check that address is generated from public key
# TODO generate private key from random words
"""

key = "ca26b1359ee7ed099d61d361390a36e4e40fcd948d6c7e41dd28e43bb08e7339"
private_key = ed25519.Ed25519PrivateKey.from_private_bytes(hex2bytes(key))
address = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                format=serialization.PublicFormat.Raw).hex()
"""


@dataclass()
class Transaction(BaseDataclass, ChainUnit):
    from_address: str
    to_address: str
    amount: int
    timestamp: float = time.time()
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
