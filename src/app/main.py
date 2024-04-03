from fastapi import FastAPI

from api import controllers, topologies
from fastapi.openapi.models import Contact,Server

# from app.api.models import Base
# from app.D_db import engine





# Base.metadata.create_all(bind=engine)

servers = [
    {
        "url": "http://localhost:8003",
        "description": "Localhost"
    },
    {
        "url": "https://api.example.com",
        "description": "Production Server"
    }
]

app = FastAPI(
    title="SDN Controller - NBI",
    description="This API manages the connection with higher-application level and GUI",
    contact=Contact(name="José Manuel Martínez Caro", url="https://www.linkedin.com/in/josemanuelmartinezcaro/", email="jmmartinez04@alu.ucam.edu"),
    version="0.0.1",
    servers= servers
    )



# app.include_router(ping.router)
# app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(controllers.router, prefix="/controllers", tags=["Controllers"])
app.include_router(topologies.router, prefix="/topologies", tags=["Topologies"])
