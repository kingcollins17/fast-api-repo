from .db import Base
from sqlalchemy import Column,String,Integer
# from sqlalchemy.orm import relationship

class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key=True,index=True)
     username = Column(String,nullable=True)
     email = Column(String, nullable=False, unique=True)
     password = Column(String,nullable=False)