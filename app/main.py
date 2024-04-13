# main.py
from fastapi import FastAPI
from api.endpoints.user import user_router


app = FastAPI()

# Include the user and item routers in the application
app.include_router(user_router, tags=["users"])
