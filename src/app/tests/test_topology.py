import json, pytest, pdb, requests
from uuid import uuid4
# from .mocks.sdn_controllers import get_tsn_topology_info, get_metro_topology_info

topology = {"network_id": "string","network_types": {},"node": [{"node_id": "string","termination_point": {},"l2_node_attributes": {},"l3_node_attributes": {}}],"link": [{"link_id": "string","source": {},"destination": {},"l2_link_attributes": {},"l3_link_attributes": {}}],"l2_topology_attributes": {},"l3_topology_attributes": {}}
topology_summary = '{"# topologies": 1,"# networks": 1,"networks": [{"network_id": "string","# nodes": 1,"# links": 1}]}'
topology_id =''


def test_get_topologies(test_app):
    response = test_app.delete("/topologies")
    response = test_app.get("/topologies")
    assert response.status_code == 200
    assert response.json() == []

def test_post_topology(test_app):
    response = test_app.post("/topologies", content=json.dumps(topology))
    assert response.status_code == 200
    response_json = response.json()
    global topology_id
    topology_id = response_json['ietf-network:networks']['topology_id']
    for net in response_json['ietf-network:networks']['network']:
        assert net == topology#{'message': 'TSN topology retrieved. Notification sent by RabbitMQ to DT'}

def test_get_topology_by_id(test_app):
    endpoint = "/topologies/"+str(topology_id)
    response = test_app.get(endpoint)
    assert response.status_code == 200
    response_json = response.json()
    # pdb.set_trace()
    for net in response_json['ietf-network:networks']['network']:   
        assert net == topology

def test_get_topology_summary(test_app):
    endpoint = "/topologies/"+str(topology_id)+'/summary'
    response = test_app.get(endpoint)
    response_json = response.json()
    # pdb.set_trace()
    assert response.status_code == 200
    assert response_json == json.loads(topology_summary)

def test_delete_topology_by_id(test_app):
    response = test_app.delete("/topologies/"+str(topology_id))
    # pdb.set_trace()
    assert response.status_code == 200
    assert response.json() == {'detail': 'Successfully deleted'}

