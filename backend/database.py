from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Alamat database untuk SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread": False} # Khusus SQLite
)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()