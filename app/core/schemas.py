

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
        extra = Extra.forbid  # Reject extra fields
        validate_all = True   # Validate all fields

class BorrowBookRequest(BaseModel):
    book_title: str
    borrowed_at: str

    class Config:
        extra = Extra.forbid

class ReturnBookRequest(BaseModel):
    book_title: str
    user_name : str
    returned_at :str 

    class Config:
        extra = Extra.forbid