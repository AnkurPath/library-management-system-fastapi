from fastapi import Depends, status ,FastAPI
from sqlalchemy.orm import Session
from core.schemas import UserCreateRequest
from core.database import DatabaseDependency
from core.models import User
from passlib.context import CryptContext
from core.service import create_access_token

user_router = FastAPI(root_path="/user")

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(create_user_request: UserCreateRequest,db: Session = Depends(DatabaseDependency())):
    create_user_model = User(
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_librarian=create_user_request.is_librarian,
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    
    access_token = create_access_token(
        data={"sub": create_user_model.email})
    return {"access_token": access_token, "token_type": "Bearer"}
