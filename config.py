import os
from configparser import ConfigParser

CONFIG_FILE = 'config.ini'


class Config:
    def __init__(self, parser: ConfigParser):
        self.parser = parser
        self.parser.read(self.config_path())

    @staticmethod
    def config_path() -> str:
        abs_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(abs_path, CONFIG_FILE)

    @property
    def cloud_database_url(self) -> str:
        return self.parser.get('DEFAULT', 'cloud_database_url')

    @property
    def local_database_url(self) -> str:
        return self.parser.get('DEFAULT', 'local_database_url')
