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
    code: int = 400
    message: str = "Bad request"

class Deleted (BaseModel):
    code: int = 200
    message: str = "Successfully deleted"