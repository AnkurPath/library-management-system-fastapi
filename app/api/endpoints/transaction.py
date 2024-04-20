from fastapi import HTTPException, status, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.schemas import BorrowBookRequest, ReturnBookRequest
from core.database import DatabaseDependency
from core.models import Book ,BorrowHistory,User
from datetime import datetime, timedelta
from core.service import get_current_user
from core.service import is_current_user_librarian

transaction_router = APIRouter(prefix="/action")

@transaction_router.post("/borrow",status_code=status.HTTP_200_OK)
async def borrow_book(
    borrow_book_request:BorrowBookRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(DatabaseDependency())
    ):
    # Checking if the book exists in the database
    book = db.query(Book).filter(Book.title == borrow_book_request.book_title).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book Not Found"
        )
    # checking book availability
    if book.availability == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is out of Stock"
        )
    book.availability = book.availability - 1
    db.commit()
    # checking if this book is already borrowed or nor 
    is_borrowed = db.query(BorrowHistory).filter(BorrowHistory.user_email == current_user.email,BorrowHistory.book_title == borrow_book_request.book_title).first()
    if is_borrowed:
       raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You already borrowed this book"
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
    

@transaction_router.post("/return",status_code=status.HTTP_202_ACCEPTED)
async def return_book(
    return_book_request:ReturnBookRequest,
    user: bool = Depends(is_current_user_librarian),
    db: Session = Depends(DatabaseDependency())
    ):
    # check the user have borrowed book or not
    is_borrowed = db.query(BorrowHistory).filter(BorrowHistory.user_email == return_book_request.user_name,BorrowHistory.book_title == return_book_request.book_title).first()

    if not is_borrowed:
       raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You have not borrowed this book"
        )
    existing_book = db.query(Book).filter(Book.title == return_book_request.book_title).first()
    existing_book.availability = existing_book.availability + 1
    existing_book.returned_at = (datetime.strptime(return_book_request.returned_at, '%Y-%m-%d') + timedelta(weeks=1)).strftime('%Y-%m-%d')
    db.commit()
