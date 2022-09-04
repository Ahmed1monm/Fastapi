from email.policy import default
import imp
from operator import index
from re import I
from sqlalchemy import Column,Boolean,Integer,String
from database import Base

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default = False)
    
