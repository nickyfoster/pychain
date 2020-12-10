import json

from redis import Redis

from utils.utils import RedisConfig, get_config


class RedisClient:
    def __init__(self, name, host, port, password):
        self.redis = Redis(host=host,
                           port=port,
                           password=password,
                           db=name)

    @classmethod
    def from_config(cls, config: RedisConfig):
        redis_client = cls(host=config.host,
                           port=config.port,
                           password=config.password)
        return redis_client


config = get_config().redis
client = Redis(password=config.password)

for x in range(4):
    client.lpush("chain", x)

res = client.lindex("chain", index=0)
all = client.lrange("chain", 0 ,-1)
print(all)
for elem in all:
    print(json.loads(elem))

print(res)
