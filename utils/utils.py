import hashlib
import inspect
import json
from dataclasses import dataclass, is_dataclass
from json import JSONDecodeError
from pathlib import Path

import yaml


@dataclass()
class BaseDataclass:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_dict(cls, d):
        return cls(**{
            k: v for k, v in d.items()
            if k in inspect.signature(cls).parameters
        })


def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


@dataclass
class BlockchainConfig:
    difficulty: int
    exclude_to_hash: list
    mining_reward: int


@nested_dataclass
class PyChainConfig:
    blockchain: BlockchainConfig


class ChainUnit:
    def __init__(self):
        pass

    def calculate_hash(self):
        return hashlib.sha256(json.dumps(self.__get_dict_from_block(), sort_keys=True).encode()).hexdigest()

    def __get_dict_from_block(self):
        _excluded_keys = get_config().blockchain.exclude_to_hash  # We exclude `hash` key when calculating block's hash
        return dict(
            (key, value)
            for (key, value) in self.__dict__.items()
            if key not in _excluded_keys
        )


def load_yml(file):
    file = Path(file)
    try:
        with file.open() as f:
            d = yaml.full_load(f)
            if d is None:
                d = dict()
    except (FileNotFoundError, JSONDecodeError):
        d = dict()
    return d


def get_config():
    return PyChainConfig(**load_yml(Path(__file__).parent / '..' / 'config.yml'))


def hex2bytes(data):
    return bytes(bytearray.fromhex(data))
