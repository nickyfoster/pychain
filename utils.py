import inspect
from dataclasses import dataclass


@dataclass()
class Payload:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_dict(cls, d):
        return cls(**{
            k: v for k, v in d.items()
            if k in inspect.signature(cls).parameters
        })
