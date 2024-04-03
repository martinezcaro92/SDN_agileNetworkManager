import requests
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient

class DatabaseHandler:
    def __init__(self, mongodb_uri, db_name, username, password):
        self.client = MongoClient(mongodb_uri, username=username, password=password)
        self.db = self.client[db_name]

    def store_data(self, data, collection_name):
        # Esto asume que los datos son un dict 
        collection = self.db[collection_name]
        collection.insert_one(data)

    def get_all_data (self, collection_name):
        collection = self.db[collection_name]
        data = []
        for col in collection.find():
            del col['_id']
            data.append(col)
        
        return data
    
    def get_controllers_ids_using_type_property (self, type_value, collection_name):
        collection = self.db[collection_name]
        data = []
        for col in collection.find({"type": type_value}):
            data.append(col['controller_id'])
        
        return data

    def get_data_by_property (self, property, property_value, collection_name):
        collection = self.db[collection_name]
        data = []
        print ("property: " + property + " | proerty_value: " + property_value)
        for col in collection.find({str(property): property_value}):
            del col['_id']
            data.append(col)

        if property=="collection_id" and len(data) > 1: return {"message": "ERROR"}
        # if len(data) == 1: return data[0]
        return data 
    
    def update_data_by_id(self, controller_id, new_data, collection_name):
        collection = self.db[collection_name]
        collection.update_one({'controller_id':controller_id}, {'$set':new_data}, upsert=False)

        data = []
        for col in collection.find({"controller_id": controller_id}):
            del col['_id']
            data.append(col)

        if len(data) > 1: return {"message": "ERROR"}
        return data[0] 

    def delete_data_by_property(self, property, property_value, collection_name):
        collection = self.db[collection_name]
        
        data = []
        for col in collection.find({str(property): property_value}):
            del col['_id']
            data.append(col)

        if len(data) != 1: return {"message": "ERROR"}
        return collection.delete_one({str(property): property_value})

    def delete_all_data(self, collection_name):
        collection = self.db[collection_name]
        res = collection.delete_many({})
        return True

