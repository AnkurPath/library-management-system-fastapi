# main.py
from fastapi import FastAPI
from core.database import Database
# from api.router import router1
from core import models
from core.database import Database
from middleware.authentication import MyMiddleware
from middleware.test import MyMiddleware2
from api.endpoints.user import user_router

models.Base.metadata.create_all(bind=Database().db_engine())

user_router.add_middleware(MyMiddleware)
user_router.add_middleware(MyMiddleware2)


app = FastAPI()

app.mount("/user",user_router)
