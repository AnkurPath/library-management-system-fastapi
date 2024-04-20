from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import SQLALCHEMY_DATABASE_URL


class Database:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

    def check_connection(self):
        try:
            with self.engine.connect():
                return True
        except OperationalError:
            return False

    def get_session(self):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return SessionLocal()

    def create_tables(self):
        Base = declarative_base()
        return Base
    
    def db_engine(self):
        return self.engine

class DatabaseDependency:
    def __init__(self):
        self.db = Database()

    def __call__(self):
        try:
            session = self.db.get_session()
            yield session
        finally:
            session.close()
