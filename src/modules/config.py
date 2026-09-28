import configparser
import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class Config:
    def __init__(self):
        config = configparser.ConfigParser()

        config_path = os.path.join(os.path.dirname(__file__), '../../configuration/config.ini')

        config.read(config_path)

        self.app_port = config['APP']['port']
        self.vault_url = config['KEYVAULT']['vault_url']
        self.backup_path = config['BACKUP']['path']

class KeyVaultConfig:
    def __init__(self, vault_url):
        try:
            credential = DefaultAzureCredential()
            self.client = SecretClient(vault_url=vault_url, credential=credential)

        except Exception as errString:
            print(f"Error initializing KeyVaultConfig: {errString}")
            raise
        else:
            print("KeyVaultConfig initialized successfully.")

    def get_secret(self, secret_name):
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as errString:
            print(f"Error retrieving secret '{secret_name}': {errString}")
            raise

class MongoInstanceConfig:
    def __init__(self, mongo_instance_id, key_vault_config):

        try:
            if not mongo_instance_id:
                raise ValueError("Mongo instance ID is required.")
            connection_string_secret_name = f"{mongo_instance_id}-connection-string"

            container_name_secret_name = f"{mongo_instance_id}-container-name"

            self.connection_string = (key_vault_config.get_secret(connection_string_secret_name))

            self.container_name = (key_vault_config.get_secret(container_name_secret_name))

        except Exception as errString:
            print(f"EFailed to load MongoDB configuration for instance" f" '{mongo_instance_id}'\n{errString}")
            raise

        else:
            print(f"MongoDB configuration for instance '{mongo_instance_id}' loaded successfully.")

        