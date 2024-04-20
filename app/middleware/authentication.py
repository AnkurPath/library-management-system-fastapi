# function for checking user is admin or not
from core.database import DatabaseDependency
from config.config import SECRET_KEY
from fastapi import Request, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from core.models import User
import jwt

class UserAuthorizationMiddleware:
    def __init__(self):
        self.secret_key = SECRET_KEY
        # Define paths to exclude from authorization
        self.exclude_paths = ["/api/user/register", "/api/user/login"]

    async def __call__(self, request: Request, db: Session = Depends(DatabaseDependency())):
        # Check if the request path is in the exclude list
        if request.url.path in self.exclude_paths:
            # Skip authorization for registration and login endpoints
            return
        else:
            # Extract the JWT token from the Authorization header
            authorization = request.headers.get("Authorization")
            if authorization is None or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
            token = authorization.split("Bearer ")[1]
            if token:
                try:
                    # Decode the token using the provided secret key
                    payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
                    user = db.query(User).filter(User.email == payload.get('sub')).first()
                    request.state.token = user
                    if user:
                        return
                    else:
                        raise HTTPException(status_code=403, detail="Unauthorized access")
                except jwt.ExpiredSignatureError:
                    raise HTTPException(status_code=401, detail="Token expired")
                except jwt.InvalidTokenError:
                    raise HTTPException(status_code=401, detail="Invalid token")
            else:
                raise HTTPException(status_code=401, detail="Authorization token missing")
