import hashlib
import json
import time

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from services.RedisClient import RedisClient
from utils.utils import hex2bytes, get_address_from_key, get_config


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
        self.seed_hex = None
        self.config = get_config()
        self.redis_client = RedisClient(self.config.redis).client
        self.redis_wallet_key_prefix = "WALLET:"

    def generate_keypair(self, seed: str) -> None:
        # TODO refactor wallet key generation
        self.seed_hex = hashlib.sha256(bytes(seed, "utf-8")).hexdigest()
        self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(hex2bytes(self.seed_hex))
        self.public_key = self.private_key.public_key()
        self.address = get_address_from_key(self.private_key)

    def get_private_key_hex(self):
        pass

    @staticmethod
    def get_private_obj_from_hex(private_key_hex):
        return ed25519.Ed25519PrivateKey.from_private_bytes(hex2bytes(private_key_hex))

    def create_wallet(self) -> bool:
        data = {
            "private_key": self.seed_hex,
            "created": time.time()
        }
        redis_wallet_name = f"{self.redis_wallet_key_prefix}{self.address}"
        exists = self.redis_client.keys(redis_wallet_name)
        if not exists:
            self.redis_client.set(redis_wallet_name, json.dumps(data))
            return True


if __name__ == '__main__':
    wallet = Wallet()
    wallet.generate_keypair("test2")
    wallet.create_wallet()
