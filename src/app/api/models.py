from pydantic import BaseModel, Field, HttpUrl
from typing import List



# Pydantic Model


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(default=8888, min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int

    class Config:
        orm_mode = True

class Controller (BaseModel):
    # id: int
    name: str = "default_name"
    description: str = "default_description"
    url: str = "https://localhost"
    port: int = 0
    username: str = "default_username"
    password: str = "default_password"
    type: str = "type_not_defined"


class ControllerWithID (BaseModel):
    controller_id: str
    name: str
    description: str
    url: str
    port: int
    username: str
    password: str
    type: str

class Node (BaseModel):
    node_id: str
    termination_point: dict
    l2_node_attributes: dict
    l3_node_attributes: dict

    def to_dict(self):
        return {
            'node_id': self.node_id,
            'termination_point': self.termination_point,
            'l2_node_attributes': self.l2_node_attributes,
            'l3_node_attributes': self.l3_node_attributes
        }

class Link (BaseModel):
    link_id: str
    source: dict
    destination: dict
    l2_link_attributes: dict
    l3_link_attributes: dict

    def to_dict(self):
        return {
            'link_id': self.link_id,
            'source': self.source,
            'destination': self.destination,
            'l2_link_attributes': self.l2_link_attributes,
            'l3_link_attributes': self.l3_link_attributes
        }

class Topology (BaseModel):
    network_id: str
    network_types: dict
    node: List[Node]
    link: List[Link]
    l2_topology_attributes: dict
    l3_topology_attributes: dict

    def to_dict(self):
        node_dicts = [node.dict() for node in self.node]
        link_dicts = [link.dict() for link in self.link]
        return {
            "network_id": self.network_id,
            "network_types": self.network_types,
            "node": node_dicts,
            "link": link_dicts,
            "l2_topology_attributes": self.l2_topology_attributes,
            "l3_topology_attributes": self.l3_topology_attributes
        }
class TopologyList (BaseModel):
    network: List[Topology]
    def to_dict(self):
        network_dicts = [network.dict() for network in self.network]
        return { "network": network_dicts}


class TopologyComplete (BaseModel):
    topology_id: str
    network: List[Topology]

    def to_dict(self):
        network_dict = [topology.to_dict() for topology in self.network]
        return {
            'ietf-network:networks': {
                "topology_id": self.topology_id,
                "network": network_dict
            }
        }


class Flow (BaseModel):
    # id: int
    name: str
    description: str
    source: int
    destination: int
    bandwidth: float
    latency: float
    type: str

class FlowWithID (BaseModel):
    id: str
    name: str
    description: str
    source: int
    destination: int
    bandwidth: float
    latency: float
    type: str


class BadRequest (BaseModel):
    detail: str = "Bad request"

class Deleted (BaseModel):
    detail: str = "Successfully deleted"