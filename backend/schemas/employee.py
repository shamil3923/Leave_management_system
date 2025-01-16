from pydantic import BaseModel

# Pydantic models
class User(BaseModel):
    name: str
    email: str
    password: str

class UserInDB(User):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    