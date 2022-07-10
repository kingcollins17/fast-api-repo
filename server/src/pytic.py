from pydantic import BaseModel,EmailStr
from typing import Optional
#all the project pydantic models...
# ------------------------------
#   USER SCHEMAS FROM PYDANTIC...
# ==============================
class User(BaseModel):
     username: str 
     email: EmailStr
     password: Optional[str]

class UserOut(BaseModel):
     username: str
     email: EmailStr
     class Config:
          orm_mode = True

class LoginUser(BaseModel):
     email: str
     password: str
# ================================