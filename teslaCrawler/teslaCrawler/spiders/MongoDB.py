from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from pymongo import MongoClient
import json


class MongoDB:
    def __init__(self, connection_string, database_name, collection_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        print("MongoDB initialised!")

    def save_json(self, json_data):
        try:
            if isinstance(json_data, dict):
                self.collection.insert_one(json_data)
            elif isinstance(json_data, list):
                self.collection.insert_many(json_data)
            else:
                raise ValueError("Input data should be a dictionary or a list of dictionaries")
            print("Data saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving data: {e}")

