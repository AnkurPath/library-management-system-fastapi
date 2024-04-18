

from pydantic import BaseModel, Extra

class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    is_librarian: bool

    class Config:
        extra = Extra.forbid

class UserLoginRequest(BaseModel):
    email: str
    password: str
    remember_me: bool

    class Config:
        extra = Extra.forbid

class AddBookRequest(BaseModel):
    title: str
    author: str
    genre: str
    availability: int

    class Config:
        extra = Extra.forbid

class UpdateBookRequest(BaseModel):
    title: str
    author: str
    genre: str
    availability: int

    class Config:
        extra = Extra.forbid

class BorrowBookRequest(BaseModel):
    book_title: str
    borrowed_at: str
#   "returned_at": "string",
#   "due_date": "string"

    class Config:
        extra = Extra.forbid
