from sqlalchemy import ForeignKey, Column, Integer, Boolean
from sqlalchemy import String

from db.engine import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    name = Column(String)
    admin = Column(Boolean, default=False)
