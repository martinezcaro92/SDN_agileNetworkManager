import json, pytest, pdb
from uuid import uuid4

request_data = {"name": "default_name", "description": "default_description", "url": "https://localhost", "port": 0, "username": "default_username", "password": "default_password", "type": "type_not_defined"}    


def test_get_controllers(test_app):
    response = test_app.get("/controllers")
    assert response.status_code == 200
    # assert response.json() == []

def test_post_controllers(test_app):
    response = test_app.post("/controllers", content=json.dumps(request_data))
    assert response.status_code == 200
    # Elimina el campo 'controller_id' de los datos de respuesta
    response_json = response.json()
    respose_json_original = response_json
    controller_id = response_json['controller_id']
    if 'controller_id' in response_json:
        del response_json['controller_id']
    assert response_json == request_data
    return controller_id, response


def test_get_controllers_by_id(test_app):
    controller_id, response_2 = test_post_controllers(test_app=test_app)
    response = test_app.get("/controllers/"+str(controller_id))
    assert response.status_code == 200
    assert response.json() == response_2.json()

def test_update_controller_by_id(test_app):
    controller_id, response_2= test_post_controllers(test_app=test_app)
    mod_req_data = request_data
    mod_req_data['name'] = 'modified name'
    # pdb.set_trace()
    response = test_app.put("/controllers/"+str(controller_id), content=json.dumps(mod_req_data))
    assert response.status_code == 200
    # Elimina el campo 'controller_id' de los datos de respuesta
    response_json = response.json()
    if len(response_json) == 1 and 'controller_id' in response_json [0]:
        response_json = response_json[0]
        del response_json['controller_id']
    assert response_json == mod_req_data

def test_delete_controller_byid(test_app):
    controller_id, response_2 = test_post_controllers(test_app=test_app)
    response = test_app.delete("/controllers/"+str(controller_id))
    assert response.status_code == 200
    assert response.json() == {"detail": "Successfully deleted"}