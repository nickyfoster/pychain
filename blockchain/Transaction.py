from dataclasses import dataclass

from utils.utils import BaseDataclass, ChainUnit


@dataclass()
class Transaction(BaseDataclass, ChainUnit):
    from_address: str
    to_address: str
    amount: int
