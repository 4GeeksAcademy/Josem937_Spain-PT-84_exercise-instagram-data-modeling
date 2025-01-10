import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy import Enum


Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True, index=True)
    firstname = Column(String(25), nullable=False)
    lastname = Column(String(25), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)

    followed_users = relationship(
        "User", 
        secondary="follower",  
        primaryjoin="User.id==follower.c.user_id",  
        secondaryjoin="User.id==follower.c.follower_id",  
        back_populates="followers"
    )

    
    followers = relationship(
        "User", 
        secondary="follower", 
        primaryjoin="User.id==follower.c.follower_id",  
        secondaryjoin="User.id==follower.c.user_id",  
        back_populates="followed_users"  
    )

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id')) 

class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum ('image', 'video', name='media_type'), nullable=False) 
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))    

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post")  
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")  

class Follower(Base):
    __tablename__ = 'follower'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)  
    follower_id = Column(Integer, ForeignKey('user.id'), primary_key=True)  
    user = relationship("User", foreign_keys=[user_id])
    follower = relationship("User", foreign_keys=[follower_id])      

class Person(Base):
    __tablename__ = 'person'
    
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
class Address(Base):
    __tablename__ = 'address'
    
    
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

    def to_dict(self):
        return {}


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
