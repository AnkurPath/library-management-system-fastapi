from fastapi import HTTPException, status, APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from core.schemas import AddBookRequest ,UpdateBookRequest
from core.database import DatabaseDependency
from core.models import Book
from core.service import is_current_user_librarian

book_router = APIRouter(prefix="/book")

@book_router.post("/add",status_code=status.HTTP_201_CREATED)
async def add_book(
    add_book_request:AddBookRequest,
    user: bool = Depends(is_current_user_librarian),
    db: Session = Depends(DatabaseDependency())
    ):
    existing_book = db.query(Book).filter(Book.title == add_book_request.title,Book.author == add_book_request.author).first()
    if existing_book:
        existing_book.availability = existing_book.availability + add_book_request.availability
        db.commit()
    else:
        new_book = Book(**add_book_request.dict())
        db.add(new_book)
        db.commit()
    
DEFAULT_PAGE_SIZE = 5

@book_router.get("/list",status_code=status.HTTP_200_OK,response_model=List[AddBookRequest])
async def get_books(
    db: Session = Depends(DatabaseDependency()),
    page: int = Query(1, gt=0),
    page_size: int = Query(DEFAULT_PAGE_SIZE, gt=0)
    ):
    offset = (page -1 ) * page_size
    books = db.query(Book).offset(offset).limit(page_size).all()
    return books

@book_router.put("/update",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(
    update_book_request:UpdateBookRequest,
    user: bool = Depends(is_current_user_librarian),
    db: Session = Depends(DatabaseDependency())
    ):
    existing_book = db.query(Book).filter(Book.title == update_book_request.title).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    existing_book.author = update_book_request.author
    existing_book.genre = update_book_request.genre
    existing_book.availability = update_book_request.availability
    db.commit()

@book_router.delete("/delete/{book_title}")
async def delete_book(
    book_title : str,
    user: bool = Depends(is_current_user_librarian),
    db: Session = Depends(DatabaseDependency())
    ):
    existing_book = db.query(Book).filter(Book.title == book_title ).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    db.delete(existing_book)
    db.commit()
    
