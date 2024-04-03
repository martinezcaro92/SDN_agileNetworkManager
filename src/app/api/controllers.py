# Importar FastAPI
from fastapi import APIRouter, HTTPException
# from src.nbi.schemas import not_found, bad_request, Controller, ControllerWithID, list_of_controllers, deleted
from api.models import NoteDB, NoteSchema, Controller, ControllerWithID, BadRequest, Deleted
from DatabaseHandler import DatabaseHandler
import json
from uuid import uuid4
from typing import List




# Inicializar FastAPI
router = APIRouter()

db = DatabaseHandler('mongodb://mongodb:27017', 'tsn-cm', 'admin', 'admin123')


# Endpoint GET /controllers
@router.get("/", description="Returns a list with all the registered controllers", summary="Return all registered controllers",
                  responses={200: {"model": List[ControllerWithID], "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
# @router.get("/", description="Returns a list with all the registered controllers", summary="Return all registered controllers",
#                 response_model=ControllerWithID, responses={400: {"model": BadRequest}})
async def get_controllers():

    try:
        res = db.get_all_data('controllers')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)
    
    return res


# Endpoint POST /controllers
# @router.post("/", description="Registers a new controller in the system", summary="Registers a new controller in the system",
#                   responses={200: {"model": ControllerWithID, "description": "Successful Response"}, 400: {"model": BadRequest, "description": "Bad Request"}})
@router.post("/", response_model=ControllerWithID, responses={400: {"model": BadRequest}})
async def post_controllers(controller: Controller):
    
    # print(controller.model_dump_json())
    # controller_w_id = controller_with_id(str(uuid), controller.name, controller.description, controller.url, controller.port, controller.username, controller.password, controller.type)
    
    try:
        controller_with_id = ControllerWithID(controller_id=str(uuid4()), name=controller.name, description=controller.description, url=controller.url, port=controller.port, username=controller.username, password=controller.password, type=controller.type)
        db.store_data(dict(controller_with_id), 'controllers')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)

    return controller_with_id
    # print(json.dumps(controller))


# Endpoint GET /controllers/tsn
@router.get("/tsn", description="Returns the controllers with type tsn", summary="Returns the controllers with type tsn",
                     responses={200: {"model": List[ControllerWithID], "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def get_tsn_controllers():

    try:
        res = db.get_data_by_property("type", "tsn",'controllers')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)
    
    return res


# Endpoint GET /controllers/metro
@router.get("/metro", description="Returns the controllers with type metro", summary="Returns the controllers with type metro",
                     responses={200: {"model": List[ControllerWithID], "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def get_tsn_controllers():

    try:
        res = db.get_data_by_property("type", "metro",'controllers')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)    
    return res



# Endpoint GET /controllers/{controller_id}
@router.get("/{controller_id}", description="Returns the parameters of a controller by id", summary="Returns the parameters of a controller by id",
                     responses={200: {"model": ControllerWithID, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def get_controllers_by_id(controller_id: str):

    try:
        res = db.get_data_by_property("controller_id",controller_id,'controllers')
        print(len(res))
        if (len(res)>1): return BadRequest
        return res[0]
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)    



# Endpoint PUT /controllers/{controller_id}
@router.put("/{controller_id}", description="Updates the parameters of an existing controller by id", summary="Updates the parameters of an existing controller by id",
                     responses={200: {"model": ControllerWithID, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def put_controllers_by_id(controller_id: str, controller: Controller):
    try:
        res = db.update_data_by_id(controller_id, dict(controller), 'controllers')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)    
    return res

# Endpoint DELETE /controllers/{controller_id}
@router.delete("/{controller_id}", description="Deletes the registered controller by id", summary="Deletes the registered controller by id",
                     responses={200: {"model": Deleted, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def delete_controllers_by_id(controller_id: str):

    try:
        res = db.delete_data_by_property('controller_id', controller_id, 'controllers')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)    
    return {'code': 200, 'message': 'Successfully deleted'}

# Endpoint DELETE /controllers/{controller_id}
@router.delete("/", description="Deletes all the registered controller by id", summary="Deletes all the registered controller by id",
                     responses={200: {"model": Deleted, "description": "Successful Response"}, 404: {"model": BadRequest, "description": "Item not found"}})
async def delete_all_controllers():

    try:
        res = db.delete_all_data('controllers')
    except Exception as e:
        print('E!: ' + str(e))
        raise HTTPException(status_code=400, detail=BadRequest)
    if res == True:    
        return {'code': 200, 'message': 'Successfully deleted'}

