from pprint import pprint

from blockchain.Blockchain import Blockchain

from blockchain.Transaction import Transaction
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from utils.utils import hex2bytes

key = "ca26b1359ee7ed099d61d361390a36e4e40fcd948d6c7e41dd28e43bb08e7339"
private_key = ed25519.Ed25519PrivateKey.from_private_bytes(hex2bytes(key))
address = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                format=serialization.PublicFormat.Raw).hex()
chain = Blockchain()

for x in range(2):
    tx = Transaction(address, "public_key", 10)
    tx.sign_transaction(private_key)
    chain.add_transaction(tx)

chain.logger.debug("Starting the miner...")
chain.mine_pending_transaction(address)
chain.mine_pending_transaction(address)

chain.mine_pending_transaction(address)
chain.logger.debug(f"Balance is: {chain.get_address_balance(address)}")
chain.logger.debug(f"Chain valid: {chain.validate_chain()}")
