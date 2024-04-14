from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    borrow_history = relationship("BorrowHistory", back_populates="user")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    author = Column(String)
    genre = Column(String)
    availability = Column(Integer)
    borrow_history = relationship("BorrowHistory", back_populates="book")

class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, ForeignKey("users.email"))
    book_title = Column(String, ForeignKey("books.title"))
    borrowed_at = Column(DateTime(timezone=True), server_default=func.now())
    returned_at = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="borrow_history")
    book = relationship("Book", back_populates="borrow_history")
