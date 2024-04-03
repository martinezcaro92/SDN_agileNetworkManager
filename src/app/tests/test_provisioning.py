import json, pytest
from uuid import uuid4


def test_get_flows(test_app):
    response = test_app.get("/flows")
    assert response.status_code == 200
    # assert response.json() == []

def test_post_flow(test_app):
    test_data = {"name": "string", "description": "string", "source": 0, "destination": 0, "bandwidth": 0, "latency": 0, "type": "string"}
    response = test_app.post("/flows", content=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == {"message": "Information retrieved"}

def test_get_flows_by_flow_id(test_app):
    flow_id = str(uuid4())
    response = test_app.get("/flows/"+str(flow_id))
    assert response.status_code == 200
    # assert response.json() == []

def test_update_flows_by_flow_id(test_app):
    flow_id = str(uuid4())
    test_data = {"name": "string", "description": "string", "source": 0, "destination": 0, "bandwidth": 0, "latency": 0, "type": "string"}
    response = test_app.put("/flows/"+str(flow_id), content=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == {"status":"TBD"}

def test_delete_flow(test_app):
    flow_id = str(uuid4())
    response = test_app.delete("/flows/"+str(flow_id))
    assert response.status_code == 200
    assert response.json() == {"code": 200, "message": "Successfully deleted"}
