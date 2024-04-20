import jwt
from datetime import datetime, timedelta
from config.config import SECRET_KEY ,ALGORITHM 
from fastapi import Depends, HTTPException, Request
from .database import DatabaseDependency
from sqlalchemy.orm import Session
from core.models import User

ACCESS_TOKEN_EXPIRE_MINUTES=30

access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
def create_access_token(data: dict, expires_delta= access_token_expires):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def is_current_user_librarian(request: Request, db: Session = Depends(DatabaseDependency())):
    user_data = request.state.token  # Assuming you have extracted and decoded the token elsewhere
    is_librarian = user_data.is_librarian
    if not is_librarian:
        raise HTTPException(status_code=401, detail="User is not a librarian")
    return True

async def get_current_user(request: Request, db: Session = Depends(DatabaseDependency())):
    user_data_email = request.state.token.email
    user = db.query(User).filter(User.email == user_data_email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
    
