from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"
class UserLogin(BaseModel):
    email: str
    password: str