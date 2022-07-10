from typing import Any, Optional
from fastapi import HTTPException,status
from passlib.context import CryptContext
from . import models
from sqlalchemy.orm import Session
from . import pytic
from .oauth2 import create_token

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#context for our hashing algorithm...//
class UserXYZ:
     # =============================================================================
     """Custom class for managing user instances and operations concerning users"""
     # =============================================================================
     def __init__(self,db: Session | None = None,username=None, email=None, password=None):
          if db:
               self.username: str | None = username
               self.email: str | None = email
               self.__password:str | None = password
               self.__db_pwd: str | None = None
               self.__exists: bool = False
               self.__db: Session | None = db
               # ==================================================================
               # self.__hashed: str | None = None  // issue with the hashing algorithm...
               # check if user is in database by default...
               # ==================================================================
               self.__check_user_in_db(self.email)
          else:
               raise Exception("Cannot Instantiate object directly")

     def get_user_data(self,username=None,email=None,password=None,hashed=False):
          if email == "email":
               return self.email
          elif password == "pwd":
               if hashed == True:
                    return self.hash_password()
               return self.__password

     def hash_password(self):
          return context.hash(self.__password)
                         
     def __verify(self):
          self.__exists = True

     def __check_user_in_db(self,email):
          """checks if user is in the database on instantiation"""
          if self.__db:
               check: Any = self.__db.query(models.User).filter(models.User.email == email).first()
               if check:
                    self.username = check.username
                    # ============================
                    # checks if user is in the database and sets the the db_pwd as the the hashed
                    # password in the database...
                    # -----------------------------------------------------------------------
                    self.__db_pwd = check.password
                    self.__verify()
          else:
               raise Exception("Database session is required for this object")
     
     def check_password(self):
          return context.verify(self.__password,self.__db_pwd)

     def login_user(self) -> dict | HTTPException:
          """
               This instance method is gonna be used to login all requesting users
               and create an access token on the fly with jwt...
               -------------------------------------------------------------------------          
          """
          if self.__exists == True and self.check_password():
               access_token = create_token(data={"user_email": self.email})
               return {"access_token":access_token,"token_type":"bearer"}
          return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid credentials")
          # ====================================================================
          # -----           -------------             ---------- - ----     ---
          # ===================================================================
     def register_user(self):
          """User registration has never been easier,lol."""
          if self.__exists == False:
               try:
                    # ===================================================================
                    pwd = self.hash_password()  #//hashing algorithm is not consistent...
                    # hashing the password before adding to the database...
                    # ===================================================================
                    if self.__db:
                         query = models.User(
                         username=self.username, email=self.email, password=pwd)
                         self.__db.add(query)
                         self.__db.commit()
                         self.__db.refresh(query)
                         # -------------------------------------------------
                         # verify that the user now exists in the database
                         # Now returning the user
                         # ==============================================================
                         # ==============================================================
                         self.__verify()
                         return query
               except Exception:
                    raise Exception("Oops!, stuff went wrong during the regisration, Perhaps.")
          return {"error": "User is already registered"}

     def __repr__(self) -> str:
          if self.email:
               return self.email
          return "Object"

     @classmethod
     def build(cls,user,db: Session):
         return cls(db,**user.dict())

     @staticmethod
     def get_user(db: Session,id=None):
          if id:
               return db.query(models.User).filter(models.User.id == id).first()
          else:
               return db.query(models.User).all()
     
# ******************************************************************************
# =============================================================================
# *****************************************************************************
# functional utilities
# def get_users(db: Session):
#      return db.query(models.User).all()

# def find_user(db: Session, **kwargs):
     
#      """find user with their email or id to see if it already exists in database"""
#      kwargs.setdefault("email", None)
#      kwargs.setdefault("id", None)

#      if kwargs["email"]:
#           user = db.query(models.User).filter(models.User.email == kwargs["email"]).first()
#           if user:
#                return user
#      elif kwargs["id"]:
#           user = db.query(models.User).filter(models.User.id == kwargs["id"]).first()
#           if user:
#                return user
# ====================================================================================

# def verify_user(req_user: pytic.LoginUser ,db: Session):
#      ctx = context.hash(req_user.password)
#      user = find_user(db,email=req_user.email)
#      if user:
#           print(user.password)
#           print(ctx)
#           if user.password == ctx:
#                return True

# def create_user(db: Session, user: pytic.User):
#     hashed_pass = context.hash(user.password)
#     user.password = hashed_pass
#     print(user.password)
#     query = models.User(**user.dict())
#     db.add(query)
#     db.commit()
#     db.refresh(query)
#     return query
