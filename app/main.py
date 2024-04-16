from fastapi import FastAPI
from core.database import Database
from core import models
from core.database import Database
from api.router import router1

models.Base.metadata.create_all(bind=Database().db_engine())

app = FastAPI()

app.include_router(router1, prefix="/api")
