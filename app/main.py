from fastapi import FastAPI ,Depends
from core.database import Database
from core import models
from core.database import Database
from api.router import router1
from middleware.authentication import UserAuthorizationMiddleware

models.Base.metadata.create_all(bind=Database().db_engine())

app = FastAPI()


# Initialize the authorization middleware
authorization_middleware = UserAuthorizationMiddleware()

# Include router1 with the /api prefix
app.include_router(router1, prefix="/api", dependencies=[Depends(authorization_middleware)])

