import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()

class DTreq (BaseModel):
    type: str = "type_of_service/traffic"
    route: list = []
    maxTraffic: float = 100
    model: str = "inter-packet time"

class DTrep (BaseModel):
    interface: str
    KPI_nom: dict
    KPI_delta: dict

class Node (BaseModel):
    node_id: str
    termination_point: dict
    l2_node_attributes: dict
    l3_node_attributes: dict

class Link (BaseModel):
    link_id: str
    source: dict
    destination: dict
    l2_link_attributes: dict
    l3_link_attributes: dict

class Topology (BaseModel):
    network_id: str
    network_types: dict
    node: Node
    link: Link
    l2_topology_attributes: dict
    l3_topology_attributes: dict

class TopologyComplete (BaseModel):
    topology_id: str
    source_controller: str
    network: List[Topology]

class Metrics (BaseModel):
    timestamp: str
    network_id: str
    latency: dict
    packet_loss: dict
    jitter: dict
    bandwidth: dict

default_metrics = {
    "timestamp": "2023-08-16T12:00:00Z",
    "network_id": "NTW12345",
    "latency": {"average": 20, "max": 50, "unit": "ms"},
    "packet_loss": {"percentage": 0.5},
    "jitter": {"average": 5, "unit": "ms"},
    "bandwidth": {
        "download": {"value": 50, "unit": "Mbps"},
        "upload": {"value": 20, "unit": "Mbps"}
    }
}

@app.get("/tsn-topology", summary="Get TSN Topology from Mocked TSN Controller")
async def get_tsn_topology_info():
    topology_tsn_data = {"ietf-network:networks":{"network":[{"network-id":"l3-tsn-domain1","network-types":{"ietf-l3-unicast-topology:l3-unicast-topology":{}},"supporting-network":[{"network-ref":"l2-wifi-tsn-domain1"},{"network-ref":"l2-wired-tsn-domain1"}],"node":[{"node-id":"L3_AGV_1","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.1"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_1","tp-ref":"Wifi-1-0-1"}]}],"supporting-node":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_1"}]},{"node-id":"L3_AGV_2","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.2"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_2","tp-ref":"Wifi-1-0-1"}]}],"supporting-node":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_2"}]},{"node-id":"L3_AGV_3","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.3"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_3","tp-ref":"Wifi-1-0-1"}]}],"supporting-node":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_3"}]},{"node-id":"L3_AGV_4","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.4"]},"supporting-termination-point":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_4","tp-ref":"Wifi-1-0-1"}]}],"supporting-node":[{"network-ref":"l2-wifi-tsn-domain1","node-ref":"Wifi-AGV_4"}]},{"node-id":"L3_Router_1","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.1.254"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-Router_1","tp-ref":"L2-1-0-1"}]},{"tp-id":"L3-1-1-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.253"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-Router_1","tp-ref":"L2-1-1-1"}]}],"suporting-node":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-Router_1"}]},{"node-id":"L3_GW_1","ietf-network-topology:termination-point":[{"tp-id":"L3-1-0-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.0.254"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-GW_1","tp-ref":"L2-1-0-1"}]},{"tp-id":"L3-1-1-1","ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["10.0.2.254"]},"supporting-termination-point":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-GW_1","tp-ref":"L2-1-1-1"}]}],"suporting-node":[{"network-ref":"l2-wired-tsn-domain1","node-ref":"L2-GW_1"}]}]},{"network-id":"l2-wifi-tsn-domain1","network-types":{"ietf-l2-topology:l2-topology":{}},"supporting-network":[{"network-ref":"l1-topo-domain1"}],"node":[{"node-id":"Wifi-AGV_1","ietf-network-topology:termination-point":[{"tp-id":"Wifi-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:d0"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_1","tp-ref":"1-0-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_1"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.1"]}},{"node-id":"Wifi-AGV_2","ietf-network-topology:termination-point":[{"tp-id":"Wifi-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:d1"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_2","tp-ref":"1-0-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_2"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.2"]}},{"node-id":"WiFi-AP_1","ietf-network-topology:termination-point":[{"tp-id":"Wifi-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:e0","tsn-attributes":{"max_data_rate":64,"buffer_size":1000,"wifi-attributes":{"bandwidth":20,"MCS":["BPSK","QPSK"]}}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AP_1","tp-ref":"1-0-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AP_1"}]},{"node-id":"Wifi-AGV_3","ietf-network-topology:termination-point":[{"tp-id":"Wifi-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:d3"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_3","tp-ref":"1-0-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_3"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.3"]}},{"node-id":"Wifi-AGV_4","ietf-network-topology:termination-point":[{"tp-id":"Wifi-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:d4"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_4","tp-ref":"1-0-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AGV_4"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.4"]}},{"node-id":"WiFi-AP_2","ietf-network-topology:termination-point":[{"tp-id":"Wifi-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:f0","tsn-attributes":{"max_data_rate":64,"buffer_size":1000,"wifi-attributes":{"bandwidth":20,"MCS":["BPSK","QPSK"]}}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AP_2","tp-ref":"1-0-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AP_2"}]}],"ietf-network-topology:link":[{"link-id":"Wifi-AGV_1,1-0-1,WiFi-AP_1,1-0-1","source":{"source-node":"Wifi-AGV_1","source-tp":"Wifi-1-0-1"},"destination":{"dest-node":"WiFi-AP_1","dest-tp":"Wifi-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Wifi-AGV_2,1-0-1,WiFi-AP_1,1-0-1","source":{"source-node":"Wifi-AGV_2","source-tp":"Wifi-1-0-1"},"destination":{"dest-node":"WiFi-AP_1","dest-tp":"Wifi-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Wifi-AGV_3,1-0-1,WiFi-AP_2,1-0-1","source":{"source-node":"Wifi-AGV_3","source-tp":"Wifi-1-0-1"},"destination":{"dest-node":"WiFi-AP_2","dest-tp":"Wifi-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Wifi-AGV_4,1-0-1,WiFi-AP_2,1-0-1","source":{"source-node":"Wifi-AGV_4","source-tp":"Wifi-1-0-1"},"destination":{"dest-node":"WiFi-AP_2","dest-tp":"Wifi-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}}]},{"network-id":"l2-wired-tsn-domain1","network-types":{"ietf-l2-topology:l2-topology":{}},"supporting-network":[{"network-ref":"l1-topo-domain1"}],"node":[{"node-id":"Wired-AP_1","ietf-network-topology:termination-point":[{"tp-id":"Wired-1-1-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:e1","tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AP_1","tp-ref":"1-1-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AP_1"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.5"]}},{"node-id":"Wired-AP_2","ietf-network-topology:termination-point":[{"tp-id":"Wired-1-1-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:f1","tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"AP_2","tp-ref":"1-1-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"AP_2"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.6"]}},{"node-id":"Wired-TSN_1","ietf-network-topology:termination-point":[{"tp-id":"Wired-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":0,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-0-1"}]},{"tp-id":"Wired-1-1-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":1,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-1-1"}]},{"tp-id":"Wired-1-2-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":2,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-2-1"}]},{"tp-id":"Wired-1-3-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":3,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-3-1"}]},{"tp-id":"Wired-1-4-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":4,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-4-1"}]},{"tp-id":"Wired-1-5-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":5,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-5-1"}]},{"tp-id":"Wired-1-6-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":6,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-6-1"}]},{"tp-id":"Wired-1-7-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":7,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1","tp-ref":"1-7-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"SW_1"}],"ietf-l2-topology:l2-node-attributes":{"management-mac":"00:00:5e:00:53:f0","management-address":["192.0.2.7"]}},{"node-id":"Wired-TSN_2","ietf-network-topology:termination-point":[{"tp-id":"Wired-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":0,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-0-1"}]},{"tp-id":"Wired-1-1-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":1,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-1-1"}]},{"tp-id":"Wired-1-2-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":2,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-2-1"}]},{"tp-id":"Wired-1-3-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":3,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-3-1"}]},{"tp-id":"Wired-1-4-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":4,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-4-1"}]},{"tp-id":"Wired-1-5-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":5,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-5-1"}]},{"tp-id":"Wired-1-6-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":6,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-6-1"}]},{"tp-id":"Wired-1-7-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":7,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2","tp-ref":"1-7-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"SW_2"}],"ietf-l2-topology:l2-node-attributes":{"management-mac":"00:00:5e:00:53:f0","management-address":["192.0.2.8"]}},{"node-id":"Wired-TSN_3","ietf-network-topology:termination-point":[{"tp-id":"Wired-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":0,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-0-1"}]},{"tp-id":"Wired-1-1-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":1,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-1-1"}]},{"tp-id":"Wired-1-2-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":2,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-2-1"}]},{"tp-id":"Wired-1-3-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":3,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-3-1"}]},{"tp-id":"Wired-1-4-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":4,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-4-1"}]},{"tp-id":"Wired-1-5-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":5,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-5-1"}]},{"tp-id":"Wired-1-6-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":6,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-6-1"}]},{"tp-id":"Wired-1-7-1","ietf-l2-topology:l2-termination-point-attributes":{"port-number":7,"tsn-attributes":{"max_data_rate":1000,"buffer_size":1000}},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3","tp-ref":"1-7-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"SW_3"}],"ietf-l2-topology:l2-node-attributes":{"management-mac":"00:00:5e:00:53:f0","management-address":["192.0.2.9"]}},{"node-id":"L2-Router_1","ietf-network-topology:termination-point":[{"tp-id":"L2-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:a0"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"Router_1","tp-ref":"1-0-1"}]},{"tp-id":"L2-1-1-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:a1"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"Router_1","tp-ref":"1-1-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"Router_1"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.10"]}},{"node-id":"L2-GW_1","ietf-network-topology:termination-point":[{"tp-id":"L2-1-0-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:b0"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"Router_2","tp-ref":"1-0-1"}]},{"tp-id":"L2-1-1-1","ietf-l2-topology:l2-termination-point-attributes":{"mac-address":"00:00:5e:00:53:b1"},"supporting-termination-point":[{"network-ref":"l1-topo-domain1","node-ref":"Router_2","tp-ref":"1-1-1"}]}],"supporting-node":[{"network-ref":"l1-topo-domain1","node-ref":"Router_2"}],"ietf-l2-topology:l2-node-attributes":{"management-address":["192.0.2.11"]}}],"ietf-network-topology:link":[{"link-id":"Wired-AP_1,1-1-1,Wired-TSN_1,1-0-1","source":{"source-node":"Wired-AP_1","source-tp":"Wired-1-1-1"},"destination":{"dest-node":"Wired-TSN_1","dest-tp":"Wired-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Wired-AP_2,1-1-1,Wired-TSN_1,1-1-1","source":{"source-node":"Wired-AP_2","source-tp":"Wired-1-1-1"},"destination":{"dest-node":"Wired-TSN_1","dest-tp":"Wired-1-1-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Wired-TSN_1,1-2-1,Wired-TSN_2,1-0-1","source":{"source-node":"Wired-TSN_1","source-tp":"Wired-1-2-1"},"destination":{"dest-node":"Wired-TSN_2","dest-tp":"Wired-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Wired-TSN_2,1-1-1,Wired-TSN_3,1-0-1","source":{"source-node":"Wired-TSN_2","source-tp":"Wired-1-1-1"},"destination":{"dest-node":"Wired-TSN_3","dest-tp":"Wired-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Router_1,1-1-1,Wired-TSN_2,1-2-1","source":{"source-node":"L2-Router_1","source-tp":"L2-1-1-1"},"destination":{"dest-node":"Wired-TSN_2","dest-tp":"Wired-1-2-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}},{"link-id":"Wired-TSN_3,1-1-1,L2-GW_1,1-0-1","source":{"source-node":"Wired-TSN_3","source-tp":"Wired-1-1-1"},"destination":{"dest-node":"L2-GW_1","dest-tp":"L2-1-0-1"},"ietf-l2-topology:l2-link-attributes":{"rate":1000,"delay":1}}]},{"network-id":"l1-topo-domain1","network-types":{"ietf-te-topology:te-topology":{}},"node":[{"node-id":"AGV_1","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"}]},{"node-id":"AGV_2","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"}]},{"node-id":"AP_1","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"},{"tp-id":"1-1-1"}]},{"node-id":"AGV_3","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"}]},{"node-id":"AGV_4","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"}]},{"node-id":"AP_2","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"},{"tp-id":"1-1-1"}]},{"node-id":"SW_1","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"},{"tp-id":"1-1-1"},{"tp-id":"1-2-1"},{"tp-id":"1-3-1"},{"tp-id":"1-4-1"},{"tp-id":"1-5-1"},{"tp-id":"1-6-1"},{"tp-id":"1-7-1"}]},{"node-id":"SW_2","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"},{"tp-id":"1-1-1"},{"tp-id":"1-2-1"},{"tp-id":"1-3-1"},{"tp-id":"1-4-1"},{"tp-id":"1-5-1"},{"tp-id":"1-6-1"},{"tp-id":"1-7-1"}]},{"node-id":"SW_3","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"},{"tp-id":"1-1-1"},{"tp-id":"1-2-1"},{"tp-id":"1-3-1"},{"tp-id":"1-4-1"},{"tp-id":"1-5-1"},{"tp-id":"1-6-1"},{"tp-id":"1-7-1"}]},{"node-id":"Router_1","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"},{"tp-id":"1-1-1"}]},{"node-id":"Router_2","ietf-network-topology:termination-point":[{"tp-id":"1-0-1"},{"tp-id":"1-1-1"}]}]}]}}

    # return json.dumps(topology_tsn_data)
    return topology_tsn_data

@app.get("/metro-topology", summary="Get Metro Topology from mocked Metro Controller")
async def get_metro_topology_info():
    topology_metro_data = {"ietf-network:networks":{"network":[{"network-id":"x","network-types":{"ietf-l2-topology:l2-topology":{},"ietf-l3-unicast-topology:l3-unicast-topology":{}},"supporting-network":[{"network-ref":"x"}],"node":[{"node-id":"x","supporting-node":[{"network-ref":"x","node-ref":"x"}],"ietf-network-topology:termination-point":[{"tp-id":"x","supporting-termination-point":[{"network-ref":"x","node-ref":"x","tp-ref":"x"}],"ietf-l2-topology:l2-termination-point-attributes":{"interface-name":"x","mac-address":"88:51:11:76:04:62","port-number":[0],"unnumbered-id":[0],"encapsulation-type":"ietf-l2-topology:qinq","outer-tag":"44,46-128,31-621","outer-tpid":"ieee802-dot1q-types:c-vlan","inner-tag":"71,45-754,26-425","inner-tpid":"ieee802-dot1q-types:c-vlan","lag":"true","member-link-tp":["x"],"vxlan":{"vni-id":0}},"ietf-l3-unicast-topology:l3-termination-point-attributes":{"ip-address":["160.151.128.30%À"]}}],"ietf-l2-topology:l2-node-attributes":{"name":"x","flags":[""],"bridge-id":["51:04:26:88:27:74:82:60"],"management-address":["167.151.144.47%۶"],"management-mac":"17:68:82:60:20:30","management-vlan":"x"},"ietf-l3-unicast-topology:l3-node-attributes":{"name":".","flag":[""],"router-id":["141.187.164.47"],"prefix":[{"prefix":"138.100.123.55/6","metric":0,"flag":[""]}]}}],"ietf-network-topology:link":[{"link-id":"x","source":{"source-node":"x","source-tp":"x"},"destination":{"dest-node":"x","dest-tp":"x"},"supporting-link":[{"network-ref":"x","link-ref":"x"}],"ietf-l2-topology:l2-link-attributes":{"name":"x","flags":[""],"rate":"0","delay":0,"auto-nego":"false","duplex":"half-duplex"},"ietf-l3-unicast-topology:l3-link-attributes":{"name":"x","flag":[""],"metric1":"0","metric2":"0"}}],"ietf-l2-topology:l2-topology-attributes":{"name":"x","flags":[""]},"ietf-l3-unicast-topology:l3-topology-attributes":{"name":"x","flag":[""]}}]}}

    # return json.dumps(topology_metro_data)
    return topology_metro_data

@app.get("/tsn-flow", summary="Get TSN flows from TSN Controller")
async def get_tsn_flow_info():
    flow_tsn_data = {"ietf-detnet:detnet":{"traffic-profile":[{"name":"TSN-1","traffic-requirements":{"min-bandwidth":"100000000","max-latency":100000000,"max-latency-variation":200000000,"max-loss":"0.0000001","max-consecutive-loss-tolerance":5,"max-misordering":0},"traffic-spec":{"interval":5,"max-pkts-per-interval":10,"max-payload-size":1500,"min-payload-size":100,"min-pkts-per-interval":1},"member-app":["tsn-app-0","tsn-app-1"]},{"name":"BE","traffic-requirements":{"min-bandwidth":"100000000","max-latency":100000000,"max-latency-variation":200000000,"max-loss":"0.1","max-consecutive-loss-tolerance":100,"max-misordering":100},"traffic-spec":{"interval":5,"max-pkts-per-interval":10,"max-payload-size":1500,"min-payload-size":100,"min-pkts-per-interval":1},"member-app":["be-app-0"]}],"app-flows":{"app-flow":[{"name":"tsn-app-0","outgoing-service":"ssl-tsn-app0","traffic-profile":"TSN-1","ingress":{"app-flow-status":"ietf-detnet:ready","interface":"eth0","tsn-app-flow":{"source-mac-address":"2001:db8::1/128","destination-mac-address":"2001:db8::8/128","vlan-id":6,"pcp":0}}},{"name":"tsn-app-1","outgoing-service":"ssl-tsn-app1","traffic-profile":"TSN-1","ingress":{"app-flow-status":"ietf-detnet:ready","interface":"eth0","tsn-app-flow":{"source-mac-address":"2001:db8::1/128","destination-mac-address":"2001:db8::8/128","vlan-id":7,"pcp":0}}},{"name":"be-app-0","outgoing-service":"ssl-be-app0","traffic-profile":"BE","ingress":{"app-flow-status":"ietf-detnet:ready","interface":"eth0","ip-app-flow":{"src-ip-prefix":"2001:db8::1/128","dest-ip-prefix":"2001:db8::8/128","vlan-id":100,"pcp":0}}}]},"service":{"sub-layer":[{"name":"ssl-tsn-app0","traffic-profile":"TSN-1","operation":"initiation","incoming":{"app-flow":{"flow":["tsn-app-0"]}},"outgoing":{"forwarding-sub-layer":{"service-outgoing":[{"index":0,"sub-layer":["fsl-app0-AP_1","fsl-app0-Wired-TSN_1","fsl-app0-Wired-TSN_2","fsl-app0-Wired-TSN_3"]}]}}},{"name":"ssl-tsn-app1","traffic-profile":"TSN-1","operation":"initiation","incoming":{"app-flow":{"flow":["tsn-app-1"]}},"outgoing":{"forwarding-sub-layer":{"service-outgoing":[{"index":0,"sub-layer":["fsl-app1-AP_2","fsl-app1-Wired-TSN_1","fsl-app1-Wired-TSN_2","fsl-app1-Wired-TSN_3"]}]}}},{"name":"ssl-be-app0","traffic-profile":"BE","operation":"initiation","incoming":{"app-flow":{"flow":["be-app-0"]}},"outgoing":{"forwarding-sub-layer":{"service-outgoing":[{"index":0,"sub-layer":["fsl-be-app0-Router_2","fsl-be-app0-Wired-TSN_2","fsl-be-app0-Wired-TSN_3","fsl-be-app0-GW_1"]}]}}}]},"forwarding":{"sub-layer":[{"name":"fsl-app0-AP_1","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":0,"outgoing-interface":"1-1-1"}]}}},{"name":"fsl-app0-Wired-TSN_1","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":1,"outgoing-interface":"1-2-1"}]}}},{"name":"fsl-app0-Wired-TSN_2","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":2,"outgoing-interface":"1-2-1"}]}}},{"name":"fsl-app0-Wired-TSN_3","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":3,"outgoing-interface":"1-1-1"}]}}},{"name":"fsl-app1-AP_2","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app1"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":0,"outgoing-interface":"1-1-1"}]}}},{"name":"fsl-app1-Wired-TSN_1","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app1"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":1,"outgoing-interface":"1-2-1"}]}}},{"name":"fsl-app1-Wired-TSN_2","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app1"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":2,"outgoing-interface":"1-2-1"}]}}},{"name":"fsl-app1-Wired-TSN_3","traffic-profile":"TSN-1","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-tsn-app1"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":3,"outgoing-interface":"1-1-1"}]}}},{"name":"fsl-be-app0-Router_1","traffic-profile":"BE","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-be-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":0,"outgoing-interface":"1-1-1"}]}}},{"name":"fsl-be-app0-Wired-TSN_2","traffic-profile":"BE","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-be-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":1,"outgoing-interface":"1-2-1"}]}}},{"name":"fsl-be-app0-Wired-TSN_3","traffic-profile":"BE","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-be-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":2,"outgoing-interface":"1-2-1"}]}}},{"name":"fsl-be-app0-GW_1","traffic-profile":"BE","operation":"forward","incoming":{"service-sub-layer":{"sub-layer":["ssl-be-app0"]}},"outgoing":{"interface":{"next_hop":[{"hop_index":3,"outgoing-interface":"1-1-1"}]}}}]}}}

    # return json.dumps(flow_tsn_data)
    return flow_tsn_data


@app.post('/topologies', summary="Post/Send the TSN and Metro topologies to Mocked DT")
async def post_dt_topology (topology: TopologyComplete):
    # print (json.loads(topology))
    return {"message": "Information retrieved", "topology": topology}

@app.post('/metrics', summary="Post/Send the device metrics to Mocked DT")
async def post_dt_topology (metrics: Metrics = default_metrics):
    # print (json.loads(metrics))
    return {"message": "Information retrieved", "metrics": metrics}

@app.post('/connectivity', summary="Post/Simulate a new request for a mocked DT simulation")
async def post_dt_topology (connectivity: DTreq):
    # print (json.loads(metrics))
    return {'KPI_nom': {'test': 1, 'latency': 0.01, 'latency_unit': "ms", 'bandwidth': 10000, 'bandwidth_unit': 'Gbps'}, 'KPI_delta': [{'interface': 'int1', 'KPI_nom': {'latency': 0.001, 'latency_unit': 'Gbps'}, 'KPI_delta':{'test': 'test1'}}]}

@app.get('/algorithms', summary="Get ENP interface to retrieve the available algorithms available (mock)")
async def get_tsn_flow_info():
    algorithms = [
        {
            "algorithmId": 0,
            "algorithmName": "Offline_nfvPlacementILP_v1",
            "algorithmDescription": "Algorithm for NFV placement"
        },
        {
            "algorithmId": 1,
            "algorithmName": "Offline_fa_ospfWeightOptimization_localSearch",
            "algorithmDescription": "Given a set of nodes, links and offered traffic, this algorithm assumes that the nodes are IP routers running the OSPF protocol (applying ECMP rules) for routing it. The algorithm searches for the set of link weights that optimize the routing. In particular, the target is minimizing a congestion metric computed as a function of both the worst-case link utilization and the average link utilization. The algorithm is based on applying a local-search heuristic approach."
        },
        {
            "algorithmId": 2,
            "algorithmName": "Offline_Example_Algorithm",
            "algorithmDescription": "Example of different parameter types."
        }
    ]
    return algorithms

@app.get('/algorithms/{algorithm_id}/input_data', summary="Get ENP interface to retrieve the available algorithms available (mock)")
async def get_algorithm_input_data_by_id(algorithm_id: int):
    if algorithm_id > 0 and algorithm_id < 4:
        return [
            {
                "first": "simpleParameter",
                "second": "Default value",
                "third": "The user may enter the desired value in a string format.",
                "modifiable": "true"
            },
            {
                "first": "booleanParameter",
                "second": "#boolean# true",
                "third": "Represents a true/false parameter through the use of a checkbox.",
                "modifiable": "true"
            },
            {
                "first": "selectParameter",
                "second": "#select# First Second Third",
                "third": "Allows the user to choose from a given array of choices.",
                "modifiable": "true"
            },
            {
                "first": "pathParameter",
                "second": "#path# Sample text",
                "third": "Brings up a file selector in order to choose a directory",
                "modifiable": "true"
            },
            {
                "first": "fileChooserParameter",
                "second": "#file# Sample text",
                "third": "Brings up a file selector in order to choose a file",
                "modifiable": "true"
            },
            {
                "first": "multipleFilesParameter",
                "second": "#files# Sample text",
                "third": "Brings up a file selector in order to choose multiple files. The files' paths are separated with the string '>'.",
                "modifiable": "true"
            }]

    else:
        raise HTTPException(status_code=404, detail='Algorithm not found (algorithm_id)')

@app.get('/algorithms={algorithm_id}/topology={topology_id}', summary="Post ENP interface to execute an algorithm for a topology")
async def post_algorithm_execution(algorithm_id: int, topology_id: int):
    # Continue developing with the response of the algorithm
    return {"message": "Algorithm excuted and finished"}

@app.get('/devices', summary="Get NMS API for list monitored devices")
async def get_monitored_devices():
    return [
        {
            "device_id":1,
            "name": "device1",
            "segment": "tsn"
        },
        {
            "device_id":2,
            "name": "device2",
            "segment": "tsn"
        },
        {
            "device_id":3,
            "name": "device3",
            "segment": "metro"
        },
        {
            "device_id":4,
            "name": "device4",
            "segment": "metro"
        }
    ]

@app.get('/devices/{device_id}/metrics', summary="Get NMS API for monitored values for a device by device_id")
async def get_monitored_metric_by_device(device_id: int):
    if device_id > 0 and device_id < 4:
        return [
            {
                "metric_id":1,
                "name": "latency",
                "last_value": 1.02,
                "last_value_unit": "ms"
            },
            {
                "metric_id":2,
                "name": "throughput",
                "last_value": 1.02,
                "last_value_unit": "Gbps"        },
            {
                "metric_id":3,
                "name": "availability",
                "last_value": 99.99951,
                "last_value_unit": "%"
            }
        ]
    else:
        raise HTTPException(status_code=404, detail='Device not found (device_id)')

@app.get('/devices={device_id}/metrics={metric_id}/values', summary="Get NMS API for last monitored values (metric_db) for a device by device_id")
async def get_monitored_metric_by_device_last_values(device_id: int, metric_id: int):
    if device_id > 0 and device_id < 4:
        if metric_id == 1:
            return [0.12, 0.25, 0.45, 0.22, 0.56, 0.23, 0.77, 0.84, 0.45, 1.02]
        elif metric_id == 2:
            return [1.25, 1.25, 2.45, 1.22, 0.56, 2.23, 0.77, 0.84, 1.45, 1.02]
        elif metric_id == 3:
            return [99.0251, 99.1254, 99.2254, 99.2354, 99.3321, 99.3698, 99.5512, 99.7512, 99.8545, 99.99951]
        else:
            raise HTTPException(status_code=404, detail='Metric not found (metric_id)')
    else:
        raise HTTPException(status_code=404, detail='Device not found (device_id)')


# # Prueba de la función
# if __name__ == "__main__":
#     topology_tsn_json = get_tsn_topology_info()
#     print(topology_tsn_json)
#     print('---------------------------------------')
#     topology_metro_json = get_metro_topology_info()
#     print(topology_metro_json)
#     print('---------------------------------------')
#     flow_tsn_json = get_tsn_flow_info()
#     print(flow_tsn_json)