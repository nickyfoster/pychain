import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from blockchain.Transaction import Transaction


class TestTransaction(unittest.TestCase):

    def test_transaction(self):
        private_key = ed25519.Ed25519PrivateKey.generate()
        address = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                        format=serialization.PublicFormat.Raw).hex()
        transaction = Transaction(to_address="",
                                  from_address=address,
                                  amount=10)
        self.run_transaction_is_valid(transaction, private_key)

    def run_transaction_is_valid(self, transaction, private_key):
        transaction.sign_transaction(private_key)
        self.assertTrue(transaction.is_valid())

