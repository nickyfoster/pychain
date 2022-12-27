import json
from uuid import uuid4

from flask import jsonify, request, Flask, session, render_template

from blockchain.Blockchain import Blockchain
from blockchain.Transaction import Transaction
from blockchain.Wallet import Wallet
from services.RedisClient import RedisClient
from utils.utils import get_config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
node_uid = str(uuid4()).replace("-", "")

config = get_config()
blockchain = Blockchain()
redis_client = RedisClient(config.redis).client


@app.route("/")
def test():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("base.html")

@app.route("/node")
def node():
    response = {
        "node": node_uid
    }
    return jsonify(response), 200


@app.route("/logout")
def logout():
    session.clear()
    return {}, 200


@app.route('/login', methods=["POST"])
def login():
    params = request.get_json()

    required_params = ["password"]
    if not all(k in params for k in required_params):
        return "Missing transaction parameters", 400

    wallet = Wallet()
    wallet.generate_keypair(params["password"])
    exists = wallet.wallet_exists()
    if exists:
        session["address"] = wallet.address
        return jsonify({
            "login_success": True,
            "address": wallet.address
        }), 200
    else:
        del wallet
        return jsonify({
            "login_success": False,
            "reason": "Wallet does not exists"
        }), 409
        pass


@app.route('/create_wallet', methods=["POST"])
def create_wallet():
    params = request.get_json()

    required_params = ["password"]
    if not all(k in params for k in required_params):
        return "Missing transaction parameters", 400

    wallet = Wallet()
    wallet.generate_keypair(params["password"])
    if wallet.create_wallet():
        return jsonify({
            "created": True,
            "address": wallet.address
        }), 200
    else:
        return jsonify({
            "created": False,
            "reason": "Wallet exists"
        }), 409
        pass


@app.route("/mine")
def mine():
    address = session.get("address")
    if address:
        mined_block = blockchain.mine_pending_transaction(mining_reward_address=address)
        return jsonify(vars(mined_block)), 200
    else:
        return jsonify({
            "reason": "Not authorized with wallet",
            "hist": "Use /login to login into your wallet"
        }), 401


@app.route("/get_balance")
def get_balance():
    address = session.get("address")
    if address:
        balance = blockchain.get_address_balance(address=address)
        return jsonify({
            "wallet_id": address,
            "balance": balance
        }), 200
    else:
        return jsonify({
            "reason": "Not authorized with wallet",
            "hist": "Use /login to login into your wallet"
        }), 401


@app.route("/chain")
def get_chain():
    chain = blockchain.get_chain()
    response = {
        "length": len(chain),
        "chain": chain
    }
    return jsonify(response), 200


@app.route("/validate")
def validate_chain():
    response = {
        "is_chain_valid": blockchain.validate_chain()
    }
    return jsonify(response), 200


@app.route("/pending_transactions")
def pending_transactions():
    pending_transactions = [transaction for transaction in blockchain.pending_transaction]
    response = {
        "pending_transactions": pending_transactions
    }
    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    params = request.get_json()

    required_params = ["from_address", "to_address", "amount"]
    if not all(k in params for k in required_params):
        return "Missing transaction parameters", 400

    wallet_data = None
    from_address = params["from_address"]
    to_address = params["to_address"]
    amount = params["amount"]

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
        return jsonify(vars(tx)), 201

    return jsonify({
        "reason": "Wallet does not exists for this address"
    }), 404
