import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import pymongo

from Network_Security.Exception import exception
from Network_Security.Logging import logger


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise exception.NetworkSecurityException(e, sys)

    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(inplace=True, drop=True)

            records = list(json.loads(data.T.to_json()).values())

            return records

        except Exception as e:
            raise exception.NetworkSecurityException(e, sys)

    def insert_data_to_mongo(self, records, database, collection_name):
        try:
            self.database = database
            self.collection_name = collection_name
            self.records = records

            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            print(f"Database: {self.database}")
            print(f"Collection: {self.collection_name}")

            self.db = self.mongo_client[self.database]
            self.collection = self.db[self.collection_name]

            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise exception.NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "Network_Security"
    COLLECTION_NAME = "Network_Data"

    networkobj = NetworkDataExtract()

    records = networkobj.csv_to_json(FILE_PATH)

    print(f"{len(records)} records found in the csv file")

    no_of_records = networkobj.insert_data_to_mongo(
        records,
        DATABASE,
        COLLECTION_NAME
    )

    print(f"{no_of_records} records inserted to MongoDB successfully")