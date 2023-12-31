from redis import Redis, exceptions

from src.utils.utils import RedisConfig


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
