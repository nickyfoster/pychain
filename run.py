from cryptography.hazmat.primitives.asymmetric import ed25519

from blockchain.Blockchain import Blockchain
from blockchain.Transaction import Transaction
from utils.utils import hex2bytes, get_address_from_key

key = "ca26b1359ee7ed099d61d361390a36e4e40fcd948d6c7e41dd28e43bb08e7339"
private_key = ed25519.Ed25519PrivateKey.from_private_bytes(hex2bytes(key))
address = get_address_from_key(private_key)
chain = Blockchain()
transaction_data = {"from_address": address, "to_address": 123, "amount": 1}

for x in range(2):
    tx = Transaction(transaction_data)
    tx.sign_transaction(private_key)
    chain.add_transaction(tx)

chain.logger.debug("Starting the miner...")
chain.mine_pending_transaction(address)
chain.mine_pending_transaction(address)

chain.mine_pending_transaction(address)
chain.logger.debug(f"Balance is: {chain.get_address_balance(address)}")
chain.logger.debug(f"Chain valid: {chain.validate_chain()}")
