# main.py
from fastapi import FastAPI
from core.database import Database
from api.endpoints.user import user_router
from core import models
from core.database import Database

models.Base.metadata.create_all(bind=Database().db_engine())

app = FastAPI()

# Include the user and item routers in the application
app.include_router(user_router, tags=["users"])
