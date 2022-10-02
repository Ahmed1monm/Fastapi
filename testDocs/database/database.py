# import SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}   #! ...is needed only for SQLite. It's not needed for other databases.
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#* Now we will use the function declarative_base() that returns a class.
#* Later we will inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base() 


