from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session
from core.schemas import UserCreateRequest,UserLoginRequest
from core.database import DatabaseDependency
from core.models import User
from passlib.context import CryptContext
from core.service import create_access_token

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_router = APIRouter(prefix="/user")

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    create_user_request: UserCreateRequest,
    db: Session = Depends(DatabaseDependency())
    ):
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
# {
#   "first_name": "ankur",
#   "last_name": "pathak",
#   "email": "ankurpathak@gmail.com",
#   "password": "abcd",
#   "is_librarian": true
# }


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    login_user_request: UserLoginRequest,
    db: Session = Depends(DatabaseDependency())
    ):
    # check for user existance
    user = db.query(User).filter(User.email == login_user_request.email).first()
    if user:
        # Verify User given password
        if bcrypt_context.verify(login_user_request.password,user.hashed_password):
            access_token = create_access_token(data={"sub":user.email})
            return {"access_token": access_token, "token_type": "Bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")
        


