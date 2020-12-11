import unittest

from cryptography.hazmat.primitives.asymmetric import ed25519

from blockchain.Blockchain import Blockchain
from blockchain.Transaction import Transaction
from utils.utils import hex2bytes, get_config, get_address_from_key


class TestBlockchain(unittest.TestCase):

    def test_blockchain(self):
        key = "ca26b1359ee7ed099d61d361390a36e4e40fcd948d6c7e41dd28e43bb08e7339"
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(hex2bytes(key))

        mock_config = get_config()

        mock_config.redis.db = 15
        chain = Blockchain(config=mock_config)
        self.run_test_blockchain(chain, private_key)

    def run_test_blockchain(self, chain, private_key):
        address = get_address_from_key(private_key)

        for x in range(2):
            data = {"from_address": address,
                    "to_address": "mock_receiver",
                    "amount": 10}
            tx = Transaction(data=data)
            print(tx)
            tx.sign_transaction(private_key)
            chain.add_transaction(tx)

        chain.mine_pending_transaction(address)
        self.assertEqual(80, chain.get_address_balance(address))
        self.assertTrue(chain.validate_chain())
        chain.delete_blockchain()
