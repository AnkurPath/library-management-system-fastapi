from fastapi import APIRouter
from api.endpoints.user import user_router
from api.endpoints.book import book_router
from api.endpoints.transaction import transaction_router

router1 = APIRouter()

router1.include_router(user_router, tags=["users"])
router1.include_router(book_router, tags=["books"])
router1.include_router(transaction_router, tags=["transactions"])