# Import required libraries
from fastapi import APIRouter, HTTPException
from fastapi.testclient import TestClient
# from src.nbi.schemas import not_found, bad_request, list_of_all_types_of_topologies, TopologyComplete, tsn_topologies, metro_topologies
from api.models import NoteDB, NoteSchema, TopologyComplete, Topology, BadRequest, Deleted, TopologyList
from typing import List
# from tests.mocks.sdn_controllers import get_tsn_topology_info, get_metro_topology_info

from DatabaseHandler import DatabaseHandler
from uuid import uuid4
import json, pika, requests


# MongoDB handler for CRUD operations
db = DatabaseHandler('mongodb://mongodb:27017', 'sdn_controller', 'admin', 'admin123')


# Inicializar FastAPI
router = APIRouter()


# Endpoint GET /topologies
@router.get("/", description="Returns all the topologies under SDN controller", summary="Return all the topologies",
                  responses={200: {"model": List[TopologyComplete], "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Item not found"}})
async def get_topologies():

    collections = ['topology']
    data = []

    try:
        for col in collections:
            results = db.get_all_data(col)

            for res in results:
                data.append(res)
        return data
    except Exception as e:
        raise HTTPException(status_code=410, detail=str(e))
    

# Endpoint GET /topologies/{topology_id}
@router.get("/{topology_id}", description="Returns updated topology info by id.", summary="Return a topology by id",
                     responses={200: {"model": TopologyComplete, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def get_topologies_by_id(topology_id: str):

    collections = ['topology']
    try:
        res = {}
        for col in collections:
            results = db.get_all_data(col)
            for res in results:
                if 'topology_id' in res['ietf-network:networks'] and res['ietf-network:networks']['topology_id']==topology_id:
                    print(res)
                    return res
        return []

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
# Endpoint POST /topologies
@router.post("/", description="Define a new topology into the system", summary="Define a new topology into the system",
                  responses={200: {"model": Topology, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def post_topology(topology: Topology):


    try:
        topologyComplete = TopologyComplete(topology_id=str(uuid4()), network= [topology])
        db.store_data(dict(topologyComplete.to_dict()), 'topology')
        return topologyComplete.to_dict()

    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)


# Endpoint DELETE /topologies/
@router.delete("/", description="Deletes all the registered controller by id", summary="Deletes all the registered controller by id",
                     responses={200: {"model": Deleted, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def delete_all_topologies():

    try:
        res = db.delete_all_data('topology')
        if res == True:    
            return {'message': 'Successfully deleted'}
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=str(e))
    

# Endpoint DELETE /topologies/{topology_id}
@router.delete("/{topology_id}", description="Deletes all the registered controller by topology_id", summary="Deletes all the registered controller by topology_id",
                     responses={200: {"model": Deleted, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def delete_topology_by_id(topology_id: str):


    collections = ['topology']
    try:
        for col in collections:
            res = db.delete_data_by_property('topology_id',topology_id, col)
            if res == {"message": "ERROR"}: raise HTTPException()
            return {'message': 'Successfully deleted'} 

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# # Endpoint GET /topologies/{topology_id}/summary
# @router.get("/{topology_id}/summary", description="Returns updated topology info by id.", summary="Return a topology by id",
#                      responses={200: {"model": TopologyComplete, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
# async def get_topologies_summary(topology_id: str):

#     collections = ['topology']
#     try:
#         res = {}
#         for col in collections:
#             results = db.get_data_summary("topology_id", str(topology_id), col)            
#         return results

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
# Endpoint GET /topologies/{topology_id}/summary
@router.get("/{topology_id}/summary", description="Returns updated topology info by id.", summary="Return a topology by id",
                     responses={200: {"model": TopologyComplete, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def get_topologies_summary(topology_id: str):

    collections = ['topology']
    try:
        res = {}
        summary = {'# topologies': 0, '# networks': 0, 'networks': []}
        for col in collections:
            results = db.get_all_data(col)
            for res in results:
                if 'topology_id' in res['ietf-network:networks'] and res['ietf-network:networks']['topology_id']==topology_id:
                    summary['# topologies']+=1
                    networks = res['ietf-network:networks']['network']
                    summary['# networks'] += len(networks)

                    for network in networks:
                        network_summary = {
                            'network_id': network.get('network_id'),
                            '# nodes': len(network.get('node', [])),
                            '# links': len(network.get('link', []))
                        }
                        summary['networks'].append(network_summary)
        return summary
        #             return res
        # return []

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint GET /topologies/{topology_id}
@router.get("/{topology_id}", description="Returns updated topology info by id.", summary="Return a topology by id",
                     responses={200: {"model": TopologyComplete, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def get_topologies_by_id(topology_id: str):

    collections = ['topology']
    try:
        res = {}
        for col in collections:
            results = db.get_all_data(col)
            for res in results:
                if 'topology_id' in res['ietf-network:networks'] and res['ietf-network:networks']['topology_id']==topology_id:
                    print(res)
                    return res
        return []

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# # Endpoint PUT /topologies/{topology_id}
# @router.put("/{topology_id}", description="Updates the parameters of an existing topology by topology_id", summary="Updates the parameters of an existing topology by topology_id",
#                      responses={200: {"model": TopologyComplete, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
# async def put_topology_by_id(topology_id: str, topology: TopologyList):
#     try:
#         res = db.update_data_by_id('topology_id', topology_id, dict(topology), 'topology')
#         return res
#     except Exception as e:
#         print('E!: ' + str(e))
#         raise HTTPException(status_code=400, detail=BadRequest)    
