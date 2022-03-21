import pandas as pd
from sqlalchemy.engine.mock import MockConnection

TABLE_NAME = 'purchases'


class PurchasesRepository:
    def __init__(self, cloud_database: MockConnection, local_database: MockConnection):
        self.cloud_database = cloud_database
        self.local_database = local_database
        self._purchases: pd.DataFrame | None = None

    def get_all(self) -> pd.DataFrame:
        if self._purchases is None:
            self._purchases = self._get_from_local()
            if self._purchases.empty:
                self._purchases = self._get_from_cloud()
                self._save_on_local()
        return self._purchases.copy()

    def _get_from_cloud(self) -> pd.DataFrame:
        with self.cloud_database.connect() as conn:
            purchases = pd.read_sql_table(TABLE_NAME, conn)[['description', 'unit']]
            purchases = purchases[['description', 'unit']]
            purchases = purchases.drop_duplicates(subset=['description']).reset_index(drop=True)
            return purchases

    def _get_from_local(self) -> pd.DataFrame:
        with self.local_database.connect() as conn:
            conn.execute(f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} (description TEXT, unit TEXT)')
            purchases = pd.read_sql_table(TABLE_NAME, conn)[['description', 'unit']]
            purchases = purchases[['description', 'unit']]
            return purchases

    def _save_on_local(self):
        with self.local_database.connect() as conn:
            self._purchases.to_sql(TABLE_NAME, conn, if_exists='replace')
