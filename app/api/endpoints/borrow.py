from fastapi import HTTPException, status, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.schemas import BorrowBookRequest
from core.database import DatabaseDependency
from core.models import Book ,BorrowHistory,User
from datetime import datetime, timedelta
from core.service import get_current_user



borrow_router = APIRouter(prefix="/action")



@borrow_router.post("/borrow")
async def borrow_book(
    borrow_book_request:BorrowBookRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(DatabaseDependency())
    ):
    # Check if the book exists in the database
    book = db.query(Book).filter(Book.title == borrow_book_request.book_title).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    if book.availability == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is out of Stock"
        )
    borrow_book_modle = BorrowHistory(
        user_email = current_user.email,
        book_title = borrow_book_request.book_title,
        borrowed_at = borrow_book_request.borrowed_at,
        returned_at = None,
        due_date = (datetime.strptime(borrow_book_request.borrowed_at, '%Y-%m-%d') + timedelta(weeks=1)).strftime('%Y-%m-%d')
        )
    db.add(borrow_book_modle)
    db.commit()
    db.refresh(borrow_book_modle)
    return borrow_book_modle
    
