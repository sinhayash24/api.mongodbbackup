from flask import Flask
from modules.config import Config
from modules.mongodb_backup import register_routes
config = Config()

app = Flask(__name__)
register_routes(app)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=config.app_port
    )
