from typing import Optional

from pydantic import BaseModel


class LoginSchema(BaseModel):
    password: Optional[str]


class TransactionSchema(BaseModel):
    from_address: Optional[str]
    to_address: Optional[str]
    amount: Optional[str]
