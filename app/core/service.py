import jwt
from datetime import datetime, timedelta

SECRET_KEY = "my-secret-key"  # Replace with your own secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Change as per your requirements

access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
def create_access_token(data: dict, expires_delta= access_token_expires):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt