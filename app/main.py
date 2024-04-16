from fastapi import FastAPI
from core.database import Database
from core import models
from core.database import Database
from api.endpoints.user import user_router

models.Base.metadata.create_all(bind=Database().db_engine())

app = FastAPI()

app.include_router(user_router, prefix="/api")
