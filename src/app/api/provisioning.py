# Importar FastAPI
from fastapi import APIRouter, HTTPException
# from src.nbi.schemas import flow, not_found, list_of_flows, bad_request, deleted
from api.models import NoteDB, NoteSchema, Flow, FlowWithID, Deleted, BadRequest
from DatabaseHandler import DatabaseHandler
# from tests.mocks.sdn_controllers import get_tsn_flow_info
import json, requests
from uuid import uuid4
from typing import List



# Inicializar FastAPI
router = APIRouter()

db = DatabaseHandler('mongodb://mongodb:27017', 'tsn-cm', 'admin', 'admin123')

# Endpoint GET /flows
@router.get("/", description="Returns a list with all the enrolled TSN flows", summary="Returns a list with all the enrolled TSN flows",
                  responses={200: {"model": List[FlowWithID], "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Item not found"}})
async def get_flows():
    
    # # TEST
    # return {"flows": "test"}


    try:
        res = db.get_all_data('tsn-flows') 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return res

# # Endpoint GET /flows/up
# @router.get("/down", description="Returns a list with all the no active TSN flows", summary="Returns a list with all the no active TSN flows",
#                      responses={200: {"model": list_of_flows, "description": "Successful Response"}, 400: {"model": bad_request, "description": "Bad Request"}})
# async def get_flows_down():

#     # Return JSON response
#     return {
#         "flows":"flows"
#     }

# # Endpoint GET /flows/down
# @router.get("/up", description="Returns a list with all the active TSN flows", summary="Returns a list with all the active TSN flows",
#                    responses={200: {"model": list_of_flows, "description": "Successful Response"}, 400: {"model": bad_request, "description": "Bad Request"}})
# async def get_flows_up():

#     # Return JSON response
#     return {
#         "flows":"flows"
#     }

# Endpoint GET /flows/{flow_id}
@router.get("/{flow_id}", description="Returns updated information of a TSN flow by id", summary="Returns updated information of a TSN flow by id",
                     responses={200: {"model": FlowWithID, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def get_flows_by_id(flow_id: str):

    try:
        res = db.get_data_by_property("flow_id",flow_id,'tsn-flows')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return res

# Endpoint POST /flows
@router.post("/", description="Creates a new flow from a source to a destination node in a TSN network based on the body data. The query returns information about the new defined TSN flow", 
                 summary="Create a new flow", responses={200: {"model": FlowWithID, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
async def post_flows(flow: Flow):

    # res = 0
    # try:
    #     res = db.get_controllers_ids("tsn",'controllers')
    #     print(res)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))


    # with open("app/api/extra/tsn-flows-example.json") as f:
    #     data = json.load(f)
  
    # data_json = json.dumps(data)
    # for i in range(len(res)):
    
    try:
        response = requests.get("http://mock:8004/tsn-flow")
        if response.status_code == 200:
            tsn_flow = response.json()
            print("Response data:", tsn_flow)
        else:
            print("Request failed with status code:", response.status_code)
        data2 = {'flow_id':str(uuid4()), 'flows': tsn_flow}
        # db.delete_data_by_property('source_controller', res[i], 'tsn-topology')
        db.store_data(data2, 'tsn-flows')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Information retrieved"}

# Endpoint PUT /flows/{flow_id}
@router.put("/{flow_id}", description="Updates an existing flow based on the body data. The query returns the updated information of the TSN flow", 
                     summary="Updates a flow by id", responses={200: {"model": FlowWithID, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def put_flows_by_id(flow_id: str, flow: Flow):

    # Return JSON response
    return {
        "status":"TBD"
    }

# Endpoint DELETE /flows/{flow_id}
@router.delete("/{flow_id}", description="Deletes an existing TSN flow by id", summary="Deletes an existing TSN flow by id",
                        responses={200: {"model": Deleted, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def delete_flows_by_id(flow_id: str):

    try:
        res = db.delete_data_by_property('flow_id', flow_id, 'tsn-flows')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {'code': 200, 'message': 'Successfully deleted'}


# Endpoint DELETE /flows
@router.delete("/", description="Deletes all the registered flows", summary="Deletes all the registered flows",
                     responses={200: {"model": Deleted, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def delete_all_controllers():

    try:
        res = db.delete_all_data('tsn-flows')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)
    if res == True:    
        return {'code': 200, 'message': 'Successfully deleted'}



