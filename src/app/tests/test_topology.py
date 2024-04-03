import json, pytest, pdb, requests
from uuid import uuid4
# from .mocks.sdn_controllers import get_tsn_topology_info, get_metro_topology_info

request_data = {"ietf-network:networks":{"network":[{"network-id":"l3-tsn-domain1","network-types":{"ietf-l3-unicast-topology:l3-unicast-topology":{}},"node":[{"node-id":"L3_AGV_1","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.1"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_1","tp-ref":"Wifi-1-0-1"}]}]},{"node-id":"L3_AGV_2","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.2"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_2","tp-ref":"Wifi-1-0-1"}]}]},{"node-id":"L3_AGV_3","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.3"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_3","tp-ref":"Wifi-1-0-1"}]}]},{"node-id":"L3_AGV_4","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.4"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_4","tp-ref":"Wifi-1-0-1"}]}]},{"node-id":"L3_Router_1","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.1.254"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-Router_1","tp-ref":"L2-1-0-1"}]},{"tp-id":"L3-1-1-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.253"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-Router_1","tp-ref":"L2-1-1-1"}]}]},{"node-id":"L3_GW_1","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.254"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-GW_1","tp-ref":"L2-1-0-1"}]},{"tp-id":"L3-1-1-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.2.254"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-GW_1","tp-ref":"L2-1-1-1"}]}]}]}]}}
tsn_controller_data = {"name": "default_TSN", "description": "default_description", "url": "https://localhost", "port": 0, "username": "default_username", "password": "default_password", "type": "tsn"}    
metro_controller_data = {"name": "default_Metro", "description": "default_description", "url": "https://localhost", "port": 0, "username": "default_username", "password": "default_password", "type": "metro"}    
tsn_topology_id = ""
metro_topology_id = ""
global tsn_topology
global metro_topology

response = requests.get("http://mock:8004/tsn-topology")
if response.status_code == 200:
    tsn_topology = response.json()
    # print("Response data:", metro_topology)

response = requests.get("http://mock:8004/metro-topology")
if response.status_code == 200:
    metro_topology = response.json()
    # print("Response data:", metro_topology)

# data_tsn_domain = ""
# with open("app/api/extra/tsn-domain-example-L123.json") as f:
#     data_tsn_domain = json.load(f)

# data_metro_domain = ""
# with open("app/api/extra/metro-domain-example.json") as f:
#     data_metro_domain = json.load(f)

def test_get_topologies(test_app):
    response = test_app.delete("/topologies")
    response = test_app.get("/topologies")
    assert response.status_code == 200
    assert response.json() == []

def test_post_tsn_topology(test_app):
    # response = test_app.delete("/topologies")
    response = test_app.post("/controllers", content=json.dumps(tsn_controller_data))
    assert response.status_code == 200
    response_json = response.json()
    if 'controller_id' in response_json:
        del response_json['controller_id']
    assert response_json == tsn_controller_data
    # return controller_id, response

    response = test_app.post("/topologies/tsn", content=tsn_topology)
    assert response.status_code == 200
    # Elimina el campo 'controller_id' de los datos de respuesta
    response_json = response.json()
    assert response_json == {'message': 'TSN topology retrieved. Notification sent by RabbitMQ to DT'}
    

def test_post_metro_topology(test_app):

    response = test_app.post("/controllers", content=json.dumps(metro_controller_data))
    assert response.status_code == 200
    response_json = response.json()
    controller_id = response_json['controller_id']
    if 'controller_id' in response_json:
        del response_json['controller_id']
    assert response_json == metro_controller_data
    # return controller_id, response

    response = test_app.post("/topologies/metro", content=metro_topology)
    assert response.status_code == 200
    # Elimina el campo 'controller_id' de los datos de respuesta
    response_json = response.json()
    assert response_json == {'message': 'Metro topology retrieved. Notification sent by RabbitMQ to DT'}

def test_get_tsn_topologies(test_app):
    global tsn_topology_id
    response = test_app.get("/topologies/tsn")
    assert response.status_code == 200
    if response.json() == []:
        assert response.json() == []
    else:
        for res in response.json():
            for res2 in res['network']:
                # pdb.set_trace()
                # assert res2 == json.loads(get_tsn_topology_info())
                assert res2 == tsn_topology
        tsn_topology_id = response.json()[0]['topology_id']

def test_get_metro_topologies(test_app):
    global metro_topology_id
    response = test_app.get("/topologies/metro")
    assert response.status_code == 200
    if response.json() == []:
        assert response.json() == []
    else:
        for res in response.json():
            for res2 in res['network']:
                # pdb.set_trace()
                # assert res2 == json.loads(get_metro_topology_info())
                assert res2 == metro_topology
        metro_topology_id = response.json()[0]['topology_id']


def test_get_tsn_topology_by_id(test_app):
    endpoint = "/topologies/"+str(tsn_topology_id)
    response = test_app.get(endpoint)
    assert response.status_code == 200
    # pdb.set_trace()
    assert response.json()['network'] == [tsn_topology]

def test_get_metro_topology_by_id(test_app):
    response = test_app.get("/topologies/"+str(metro_topology_id))
    assert response.status_code == 200
    assert response.json()['network'] == [metro_topology]
