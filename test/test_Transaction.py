import unittest

from cryptography.hazmat.primitives.asymmetric import ed25519

from blockchain.Transaction import Transaction
from utils.utils import get_address_from_key


class TestTransaction(unittest.TestCase):

    def test_transaction(self):
        private_key = ed25519.Ed25519PrivateKey.generate()
        address = get_address_from_key(private_key)
        data = {"from_address": address,
                "to_address": "mock_receiver",
                "amount": 10}
        tx = Transaction(data=data)
        self.run_transaction_is_valid(tx, private_key)

    def run_transaction_is_valid(self, transaction, private_key):
        transaction.sign_transaction(private_key)
        self.assertTrue(transaction.is_valid())
