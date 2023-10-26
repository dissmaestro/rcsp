"""Database for todo
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session  #pylint: disable=unused-import
from sqlalchemy.exc import OperationalError

from models import Base

DB_PATH = "../data"
DB_URL = f"sqlite:///{DB_PATH}/db.sqlite"

ENGINE = create_engine(DB_URL, connect_args={"check_same_thread": False})
# for logging all SQL-queries
#ENGINE = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
SESSIONLOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

def init_db():
    """Init database, create all models as tables
    """
    if not os.path.exists(DB_PATH):
        os.mkdir(DB_PATH)

    # check_same_thread is for SQLite only
    Base.metadata.create_all(bind=ENGINE)


def get_db():
    """Create session/connection for each request
    """
    database = SESSIONLOCAL()
    try:
        yield database
    finally:
        database.close()
