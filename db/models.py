from sqlalchemy import ForeignKey, Column, Integer, Boolean, String, Text
from sqlalchemy.orm import relationship

from db.engine import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    name = Column(String)
    admin = Column(Boolean, default=False)


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    admin = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users")


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users")
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Groups")
