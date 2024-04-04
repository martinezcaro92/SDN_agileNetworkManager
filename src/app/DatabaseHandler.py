import requests
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient
from api.models import Node

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
        print ("property: " + property + " | property_value: " + property_value)
        for col in collection.find({str(property): property_value}):
            del col['_id']
            data.append(col)

        if property=="collection_id" and len(data) > 1: return {"message": "ERROR"}
        # if len(data) == 1: return data[0]
        return data 


    def update_data_by_id(self, property, property_value, new_data, collection_name):
        print('new_data')
        print(new_data)
        new_data_serializable = {}
        for key, value in new_data.items():
            print ('key: ' + str(key) + ' | value: ' + str(value))
            if key == 'node' or key == 'link':
                for v in value: 
                    new_data_serializable[key] = v.to_dict()
            else:
                new_data_serializable[key] = value
        print('new_data_serializable')
        print(new_data_serializable)

        # Luego puedes realizar la actualización utilizando new_data_serializable en lugar de new_data
        collection = self.db[collection_name]
        filter_query = {property: property_value}
        update_data = {}
        if collection_name == 'topology': update_data = {'$set': {'ietf-network:networks': {'network': [new_data_serializable]}}}
        else: update_data = {'$set': new_data_serializable}
        collection.update_one(filter_query, update_data, upsert=False)
    
        data = []
        for col in collection.find({property: property_value}):
            del col['_id']
            data.append(col)

        print('data')
        print(data)
        if len(data) > 1: return {"message": "ERROR"}

        return data  

    def delete_data_by_property(self, property, property_value, collection_name):
        collection = self.db[collection_name]
        
        data = []
        # data = collection.find_one({f"ietf-network:networks.{str(property)}": property_value})
        # for col in collection.find({str(property): property_value}):
        for col in collection.find({f"ietf-network:networks.{str(property)}": property_value}):
            del col['_id']
            data.append(col)

        if len(data) != 1: return {"message": "ERROR"}
        return collection.delete_one({f"ietf-network:networks.{str(property)}": property_value})

    def delete_all_data(self, collection_name):
        collection = self.db[collection_name]
        res = collection.delete_many({})
        return True
    
    

