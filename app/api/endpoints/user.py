from fastapi import APIRouter, Depends, status ,FastAPI
from sqlalchemy.orm import Session
from core.schemas import UserCreateRequest
from core.database import DatabaseDependency
from core.models import User

user_router = FastAPI(openapi_prefix="/user")

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(create_user_request: UserCreateRequest,db: Session = Depends(DatabaseDependency())):
    create_user_model = User(
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        email=create_user_request.email,
        hashed_password=create_user_request.password,
        is_librarian=create_user_request.is_librarian,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model
