from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from core.database import Database

database= Database()
Base = database.create_tables()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_librarian = Column(Boolean)
    borrow_history = relationship("BorrowHistory", back_populates="user")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), unique=True, index=True)
    author = Column(String(255))
    genre = Column(String(255))
    availability = Column(Integer)
    borrow_history = relationship("BorrowHistory", back_populates="book")

class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(255), ForeignKey("users.email"),index=True)
    book_title = Column(String(255), ForeignKey("books.title"))
    borrowed_at = Column(TIMESTAMP, server_default=func.now())
    returned_at = Column(TIMESTAMP, nullable=True)
    due_date = Column(TIMESTAMP)

    user = relationship("User", back_populates="borrow_history")
    book = relationship("Book", back_populates="borrow_history")
