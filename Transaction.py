from dataclasses import dataclass

from utils import Payload


@dataclass()
class Transaction(Payload):
    from_address: str
    to_address: str
    amount: int
