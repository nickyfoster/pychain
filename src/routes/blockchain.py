import json
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi import Response

from src.auth.session import SessionData, backend, cookie, verifier
from src.blockchain.Blockchain import Blockchain
from src.blockchain.Transaction import Transaction
from src.blockchain.Wallet import Wallet
from src.schemas.schemas import LoginSchema, TransactionSchema
from src.services.RedisClient import RedisClient
from src.utils.utils import get_config

node_uid = str(uuid4()).replace("-", "")

config = get_config()
blockchain = Blockchain()
redis_client = RedisClient(config.redis).client

router = APIRouter()


@router.get("/node")
def node():
    response = {
        "node": node_uid
    }
    return response


@router.post('/create_wallet')
async def create_wallet(login_data: LoginSchema, response: Response):
    wallet = Wallet()
    wallet.generate_keypair(login_data.password)
    if wallet.create_wallet():
        this_session = uuid4()
        data = SessionData(wallet_address=wallet.address)
        await backend.create(this_session, data)
        cookie.attach_to_response(response, this_session)
        return {
            "created": True,
            "address": wallet.address
        }
    else:
        return {
            "created": False,
            "reason": "Wallet exists"
        }


@router.get("/mine", dependencies=[Depends(cookie)])
def mine(session_data: SessionData = Depends(verifier)):
    address = session_data.wallet_address

    if address:
        mined_block = blockchain.mine_pending_transaction(mining_reward_address=address)
        return vars(mined_block)
    else:
        return {
            "reason": "Not authorized with wallet",
            "hist": "Use /login to login into your wallet"
        }


@router.get("/get_balance", dependencies=[Depends(cookie)])
def get_balance(session_data: SessionData = Depends(verifier)):
    address = session_data.wallet_address

    if address:
        balance = blockchain.get_address_balance(address=address)
        return {
            "wallet_id": address,
            "balance": balance
        }
    else:
        return {
            "reason": "Not authorized with wallet",
            "hist": "Use /login to login into your wallet"
        }


@router.get("/chain")
def get_chain():
    chain = blockchain.get_chain()
    response = {
        "length": len(chain),
        "chain": chain
    }
    return response


@router.get("/validate")
def validate_chain():
    response = {
        "is_chain_valid": blockchain.validate_chain()
    }
    return response


@router.get("/pending_transactions")
def pending_transactions():
    _pending_transactions = [transaction for transaction in blockchain.pending_transaction]
    response = {
        "pending_transactions": _pending_transactions
    }
    return response


@router.post("/transactions/new")
def new_transaction(transaction: TransactionSchema):
    wallet_data = None
    from_address = transaction.from_address
    to_address = transaction.to_address
    amount = transaction.amount

    current_addresses = redis_client.keys("WALLET:*")
    for addr in current_addresses:
        if from_address == addr.decode()[7:]:
            wallet_data = json.loads(redis_client.get(f"WALLET:{from_address}"))
            break
    if wallet_data:
        data = {"from_address": from_address,
                "to_address": to_address,
                "amount": amount}
        tx = Transaction(data=data)
        tx.sign_transaction(Wallet.get_private_obj_from_hex(wallet_data["private_key"]))

        blockchain.add_transaction(tx)
        return vars(tx)

    return {
        "reason": "Wallet does not exists for this address"
    }
