from uuid import uuid4

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from flask import jsonify, request, Flask
from flask_classy import FlaskView, route

from blockchain.Blockchain import Blockchain
from blockchain.Transaction import Transaction
from utils.utils import hex2bytes

app = Flask(__name__)


class BlockchainAPI:

    def __init__(self):
        self.node_uid = str(uuid4()).replace("-", "")
        self.blockchain = Blockchain()
        self.address = None
        self.private_key = None

    @app.route("/node")
    def node(self):
        response = {
            "node": self.node_uid
        }
        return jsonify(response), 200

    @app.route('/login', methods=["POST"])
    def login(self):
        pass

    @app.route("/mine")
    def mine(self):
        mined_block = self.blockchain.mine_pending_transaction(mining_reward_address=None)
        print(self.blockchain.chain)
        return jsonify(vars(mined_block)), 200

    @app.route("/chain")
    def get_chain(self):
        print(self.blockchain.chain)
        response = {
            "chain": self.blockchain.chain,
            "length": len(self.blockchain.chain),
        }
        return jsonify(response), 200

    # @route("/transactions/new", methods=["POST"])
    # def new_transaction(self):
    #     params = request.get_json()
    #
    #     required_params = ['from_address', 'to_address', 'amount']
    #     if not all(k in params for k in required_params):
    #         return 'Missing transaction parameters', 400
    #
    #     private_key = ed25519.Ed25519PrivateKey.from_private_bytes(hex2bytes(key))
    #     address = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
    #                                                     format=serialization.PublicFormat.Raw).hex()
    #
    #     tx = Transaction(from_address=params["from_address"],
    #                      to_address=params["to_address"],
    #                      amount=params["amount"])
    #     tx.sign_transaction(private_key)
    #
    #     self.blockchain.add_transaction(tx)
    #     return jsonify(vars(tx)), 201
