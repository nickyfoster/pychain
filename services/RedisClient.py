import json

from redis import Redis, exceptions

from utils.utils import RedisConfig, get_config


class RedisClient:
    def __init__(self, client_config: RedisConfig):
        self.client = Redis(host=client_config.host,
                            port=client_config.port,
                            db=client_config.db,
                            password=client_config.password)

        try:
            self.client.keys()
        except (exceptions.ConnectionError, ConnectionRefusedError):
            raise Exception("Failed to connect to Redis server")


if __name__ == '__main__':
    client = RedisClient(get_config().redis).client
    current_addresses = client.keys("WALLET:*")
    for addr in current_addresses:
        print()
        # res =
        # print(res)
