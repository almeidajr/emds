from configparser import ConfigParser
from typing import Final

from sqlalchemy import create_engine
from sqlalchemy.engine.mock import MockConnection

from config import Config
from repositories.purchases_repository import PurchasesRepository
from services.google_service import GoogleService
from services.html_service import HtmlService


class Container:
    def __init__(self):
        self.configParser: Final[ConfigParser] = ConfigParser()
        self.config: Final[Config] = Config(parser=self.configParser)
        self.cloud_database: Final[MockConnection] = create_engine(url=self.config.cloud_database_url)
        self.local_database: Final[MockConnection] = create_engine(url=self.config.local_database_url)
        self.purchases_repository: Final[PurchasesRepository] = PurchasesRepository(
            cloud_database=self.cloud_database,
            local_database=self.local_database,
        )
        self.html_service: Final[HtmlService] = HtmlService()
        self.google_service: Final[GoogleService] = GoogleService(html_service=self.html_service)
