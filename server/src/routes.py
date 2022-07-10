# route for api...
from fastapi import APIRouter,Depends,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from .pytic import User,LoginUser,UserOut
from .db import get_db
from sqlalchemy.orm import Session
from . import models
from .utils import UserXYZ
from . import oauth2


router = APIRouter()

@router.post('/register',status_code=status.HTTP_201_CREATED,response_model=UserOut)
def handler(user: User, db: Session = Depends(get_db)):
     # creating a new user using our UserXYZ Manager class
     user_obj = UserXYZ.build(user,db)
     # cannot intantiate the object directly.
     reg_user = user_obj.register_user()
     return reg_user

@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
     log_user = UserXYZ.build(user,db)
     return log_user.login_user()
     # --------------------------
     # All logic has been implemented in the UserXYZ class...
     # =============================

@router.get('/users')
def users(id: int | None = None ,db: Session = Depends(get_db),
               current_user = Depends(oauth2.get_current_user)):
     if id:
          return UserXYZ.get_user(db,id)
     else:
         return {"user": current_user, "data": UserXYZ.get_user(db)}


