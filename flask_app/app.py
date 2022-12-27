from flask import session

from flask_app.BlockchainAPI import app
from services.RedisClient import RedisClient
from utils.utils import get_config

config = get_config()
app.secret_key = config.server.secret_key
app.config['SESSION_TYPE'] = config.server.session_type

if config.server.session_type == "redis":
    app.config['SESSION_REDIS'] = RedisClient(config.redis).client

if __name__ == '__main__':
    app.run(host=config.server.host, port=5005)
