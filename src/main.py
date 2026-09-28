from flask import Flask
from modules.config import (Config, KeyVaultConfig)
from modules.mongodb_backup import register_routes
config = Config()
key_vault_config = KeyVaultConfig(config.vault_url)

app = Flask(__name__)
register_routes(app, key_vault_config)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=config.app_port
    )
