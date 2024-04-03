# DEFINE IT ACCORDING TO DT INTERFACE
# Importamos las bibliotecas necesarias
import requests
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient

# Clase para gestionar las peticiones a la API
class APIHandler:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password) if username and password else None

    def get_data(self, endpoint, params=None):
        # Crea la url completa
        url = f"{self.base_url}/{endpoint}"
        print(url)

        # Realiza la petición
        response = requests.get(url, params=params, auth=self.auth)

        # Asegúrate de que la petición fue exitosa
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        return response.json()

# Clase para gestionar la base de datos
class DatabaseHandler:
    def __init__(self, mongodb_uri, db_name, username, password):
        self.client = MongoClient(mongodb_uri, username=username, password=password)
        self.db = self.client[db_name]

    def store_data(self, data, collection_name):
        # Esto asume que los datos son un dict 
        collection = self.db[collection_name]
        collection.insert_one(data)



def main():
    # Crear una instancia de APIHandler
    api = APIHandler('http://localhost:8080', 'mi_usuario', 'mi_contraseña')

    # Crear una instancia de DatabaseHandler
    db = DatabaseHandler('mongodb://localhost:27017', 'flows', 'admin', 'admin123')

    # Obtener datos de la API
    data = api.get_data('flows')

    # Almacenar los datos en la base de datos
    db.store_data(data, 'flows')

if __name__ == '__main__':
    main()
