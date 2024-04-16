from pydantic import BaseModel 

class UserCreateRequest(BaseModel):
    first_name :str
    last_name : str
    email : str
    password : str
    is_librarian : bool

class UserLoginRequest(BaseModel):
    email : str
    password : str
    remember_me : bool

class AddBookRequest(BaseModel):
    title : str
    author : str
    genre : str
    availability : int


class UpdateBookRequest(BaseModel):
    title : str
    author : str
    genre : str
    availability : int