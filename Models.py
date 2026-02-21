from sqlalchemy import Column, Integer, String, ForeignKey
from .Database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    Creator = relationship('user', back_populates = 'blogs')

class user(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    Password = Column(String)

    blogs = relationship('Blog', back_populates = 'Creator')