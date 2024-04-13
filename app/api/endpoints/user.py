from fastapi import APIRouter 
from fastapi.responses import JSONResponse

user_router = APIRouter(prefix="/user")

with open("D:\library-management-system-fastapi\MOCK_DATA.json","r") as f:
    data= f.read()

@user_router.get("/userlist")
async def get_all_user():
    return JSONResponse(data)


@user_router.post("/register")
async def register_user():
    pass