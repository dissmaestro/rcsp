"""Todo models
"""
from enum import Enum

from sqlalchemy import Column, Integer, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tags(str, Enum):
    study = "учёба"
    personal = "личное"
    plans = "планы"


class Todo(Base):
    """Todo model
    """
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(Text)
    completed = Column(Boolean, default=False)
    tag = Column(Text, default=Tags.plans)

    def __repr__(self):
        return f'<Todo {self.id}>'
