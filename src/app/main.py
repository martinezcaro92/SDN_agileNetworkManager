from fastapi import FastAPI

from api import provisioning, controllers, topologies
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
    title="TSN Connectivity Manager - NorthBound Interface API",
    description="This API manages the connection with higher-application level and GUI",
    contact=Contact(name="Contact", url="https://timing.upc.edu/"),#, email="efernandez@e-lighthouse.com"),
    version="0.0.1",
    servers= servers
    )



# app.include_router(ping.router)
# app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(provisioning.router, prefix="/flows", tags=["Provisioning"])
app.include_router(controllers.router, prefix="/controllers", tags=["Controllers"])
app.include_router(topologies.router, prefix="/topologies", tags=["Topologies"])
