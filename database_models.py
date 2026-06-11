from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Task(Base):
    
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean)
    created_at = Column(String)
   
    user_id = Column(Integer, ForeignKey("user.id"))
    
    user = relationship("User", back_populates="tasks")
    
class User(Base):
    
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    
    tasks = relationship("Task", back_populates="user")