from abc import ABC, abstractmethod
import psycopg2
import sys
import os
from sqlalchemy import create_engine
import pandas as pd


class WriterAbs(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def write(self):
        pass


class PostgreSQLDatabase:
    def __init__(self):
        try:
            self.dbname = os.environ.get("POSTGRES_DATABASE")
            self.host = os.environ.get("POSTGRES_URL")
            self.port = os.environ.get("POSTGRES_PORT")
            self.user = os.environ.get("POSTGRES_USER")
            self.table = os.environ.get("POSTGRES_TABLE")
            self.pwd = os.environ.get("POSTGRES_PW")


        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def write(self, data):
        """
        This functions uploads a dataframe to the target table
        :param data: DataFrame
        """
        try:
            df = pd.DataFrame(data.items(), columns=['user', 'result'])
            print("Connecting to Database")
            conn = psycopg2.connect(database=self.dbname, host=self.host, port=self.port,
                                    user=self.user, password=self.pwd)
            url = f'postgresql://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.dbname}'
            engine = create_engine(url)
            data.to_sql(self.table, engine, method='multi', if_exists='append', schema='dev', index=False,
                        chunksize=1000)
            rows = len(data)
            print(f"{rows} rows moved to the database")
            conn.close()
            print("DB connection closed.")
        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)
