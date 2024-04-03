# Import required libraries
from fastapi import APIRouter, HTTPException
from fastapi.testclient import TestClient
# from src.nbi.schemas import not_found, bad_request, list_of_all_types_of_topologies, TopologyComplete, tsn_topologies, metro_topologies
from api.models import NoteDB, NoteSchema, TopologyComplete, Topology, BadRequest, Deleted
from typing import List
# from tests.mocks.sdn_controllers import get_tsn_topology_info, get_metro_topology_info


from DatabaseHandler import DatabaseHandler
from uuid import uuid4
import json, pika, requests


# MongoDB handler for CRUD operations
db = DatabaseHandler('mongodb://mongodb:27017', 'tsn-cm', 'admin', 'admin123')


# Inicializar FastAPI
router = APIRouter()


# Endpoint GET /topologies
@router.get("/", description="Returns all the information about the underlaying network topologies in different segments and domains", summary="Return all the topologies",
                  responses={200: {"model": List[TopologyComplete], "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Item not found"}})
async def get_topologies():

    collections = ['metro-topology','tsn-topology']
    data = []

    try:
        for col in collections:
            results = db.get_all_data(col)

            for res in results:
                data.append(res)
        # print(res)
    except Exception as e:
        raise HTTPException(status_code=410, detail=str(e))
    
    return data

# Endpoint GET /topologies/tsn
@router.get("/tsn", description="Returns a list with the network topologies from the underlying TSN Controllers", summary="Return all TSN topologies",
                     responses={200: {"model": List[TopologyComplete], "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def get_topologies_tsn():

    try: 
        res = db.get_all_data('tsn-topology')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return res

# Endpoint GET /topologies/metro
@router.get("/metro", description="Returns a list with the network topologies from the underlying Metro Controllers.", summary="Return all Metro topologies",
                   responses={200: {"model": List[TopologyComplete], "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def get_topologies_metro():

    try: 
        res = db.get_all_data('metro-topology')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return res

# Endpoint GET /topologies/{topology_id}
@router.get("/{topology_id}", description="Returns updated information from a network (included in TSN or Metro topology) by id.", summary="Return a topology by id",
                     responses={200: {"model": TopologyComplete, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def get_topologies_by_id(topology_id: str):

    collections = ['metro-topology','tsn-topology']
    try:
        for col in collections:
            results = db.get_all_data(col)

            for res in results:
                if 'topology_id' in res and res['topology_id']==topology_id:
                    print(res)
                    return res
        return []
                # data.append(res)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"error": "error"}
    
# Endpoint POST /topologies/tsn
@router.post("/tsn", description="Downloads the TSN topology and uploads it to database", summary="Downloads the TSN topology and uploads it to database",
                  responses={200: {"model": Topology, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def post_tsn_topology():

    res = 0
    try:
        res = db.get_controllers_ids_using_type_property("tsn",'controllers')
        if res == []: 
            print('E!: No previously registered TSN controlers in the system')
            return []
    except Exception as e:
        raise HTTPException(status_code=400, detail=BadRequest)


    # with open("app/api/extra/tsn-domain-example-L123.json") as f:
    #     data = json.load(f)
  
    data2 = []
    data3 = []
    for i in range(len(res)):
        response = requests.get("http://mock:8004/tsn-topology")
        if response.status_code == 200:
            tsn_topology = response.json()
            print("Response data:", tsn_topology)
        else:
            print("Request failed with status code:", response.status_code)
        data2 = {'topology_id':str(uuid4()), 'source_controller': str(res[i]), 'type':'tsn', 'network': [tsn_topology]}
        data3.append(data2)
        try:
            db.delete_data_by_property('source_controller', res[i], 'tsn-topology')
            db.store_data(data2, 'tsn-topology')
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    print(len(data3))

    try:
        # RabbitMQ settings
        credentials = pika.PlainCredentials('admin', 'admin123')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='host.docker.internal', credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='topology-tsn')

        channel.basic_publish(exchange='', routing_key='topology-tsn', body=str(data3))
        print(" [x] Sent TSN Topology to the DT")
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "TSN topology retrieved. Notification sent by RabbitMQ to DT"}


# Endpoint POST /topologies/metro
@router.post("/metro", description="Downloads the Metro topology and uploads it to database", summary="Downloads the Metro topology and uploads it to database",
                  responses={200: {"model": Topology, "description": "Successful Response"}, 400: {"model":BadRequest, "description": "Bad Request"}})
async def post_metro_topology():
    
    res = 0
    try:
        res = db.get_controllers_ids_using_type_property("metro",'controllers')
        if res == []: 
            print('E!: No previously registered Metro controlers in the system')
            return []
    except Exception as e:
        raise HTTPException(status_code=400, detail=BadRequest)

    data2 = []
    data3 = []
    for i in range(len(res)):
        response = requests.get("http://mock:8004/metro-topology")
        if response.status_code == 200:
            metro_topology = response.json()
            print("Response data:", metro_topology)
        else:
            print("Request failed with status code:", response.status_code)
        data2 = {'topology_id':str(uuid4()), 'source_controller': str(res[i]), 'type':'metro', 'network': [metro_topology]}
        data3.append(data2)
        try:
            db.delete_data_by_property('source_controller', res[i], 'metro-topology')
            db.store_data(data2, 'metro-topology')
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    try:
        # RabbitMQ settings
        credentials = pika.PlainCredentials('admin', 'admin123')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='host.docker.internal', credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='topology-metro')
        channel.basic_publish(exchange='', routing_key='topology-metro', body=str(data3))
        print(" [x] Sent Metro Topology to the DT")
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Metro topology retrieved. Notification sent by RabbitMQ to DT"}

# Endpoint DELETE /topologies/
@router.delete("/", description="Deletes all the registered controller by id", summary="Deletes all the registered controller by id",
                     responses={200: {"model": Deleted, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def delete_all_controllers():

    try:
        res = db.delete_all_data('metro-topology')
        res = db.delete_all_data('tsn-topology')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)
    if res == True:    
        return {'code': 200, 'message': 'Successfully deleted'}

# Endpoint DELETE /topologies
@router.delete("/", description="Deletes all the registered controller by id", summary="Deletes all the registered controller by id",
                     responses={200: {"model": Deleted, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def delete_all_topologies():

    try:
        res = db.delete_all_data('metro-topology')
        res = db.delete_all_data('tsn-topology')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)
    if res == True:    
        return {'code': 200, 'message': 'Successfully deleted'}

