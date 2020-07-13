from abc import ABC, abstractmethod
from google.cloud import bigquery
import pandas as pd
from sqlalchemy import MetaData, Table
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
import sys

import injector


class RetrieverAbs(ABC, injector.Module):
    def __init__(self):
        pass

    @abstractmethod
    def get(self):
        pass


class BigQuery(RetrieverAbs):

    def __init__(self):
        # Establish connection to the server
        super().__init__()

        self.gcp_project = bigquery.Client().project
        self.dataset = "my_dataset"
        self.table = "my_table"
        bigquery_uri = f"bigquery://{self.gcp_project}/{self.dataset}"

        self.engine = create_engine(bigquery_uri)

    def get(self, user):
        """
        This functions gets the input data for our machine learning model
        :param user: str
        :return: DataFrame
        """
        try:
            print("Connecting to Database")
            # Establish the connection
            conn = self.engine.connect()
            metadata = MetaData()
            table = Table(f"{self.gcp_project}.{self.dataset}.{self.table}", metadata, autoload=True,
                          autoload_with=self.engine)
            # Set up the query
            query = select(table.columns["data"]).select_from(table).where(
                table.columns["user"] == user)
            # Retrieve the data
            df = pd.read_sql_query(query, self.engine)
            # Close the connection
            conn.close()
            print("DB connection closed.")
            return df
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)
