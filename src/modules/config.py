import configparser
import os

class Config:
    def __init__(self):
        config = configparser.ConfigParser()

        config_path = os.path.join(os.path.dirname(__file__), '../../configuration/config.ini')

        config.read(config_path)

        self.mongo_host = config['MONGO']['host']
        self.mongo_port = config['MONGO']['port']

        self.backup_path = config['BACKUP']['path']

        self.app_port = int(config['APP']['port'])