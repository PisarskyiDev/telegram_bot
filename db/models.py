from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Boolean,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship

from db.engine import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    name = Column(String)
    admin = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    chats_user = relationship(
        "Chats",
        back_populates="user",
        innerjoin=True,
    )
    messages_user = relationship(
        "Messages",
        back_populates="user",
        innerjoin=True,
    )


class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        Users,
        back_populates="chats_user",
        innerjoin=True,
    )


class Messages(Base):
    __tablename__ = "messages"
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=False,
    )
    date = Column(DateTime, default=datetime.now)
    question = Column(Text)
    answer = Column(Text, nullable=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        Users,
        back_populates="messages_user",
        innerjoin=True,
    )
