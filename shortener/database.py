# The module contains information about your database connection

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_db_settings

# engine = create_engine(
#     get_settings().db_url, connect_args={"check_same_thread": False}
# )

settings = get_db_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.username}:{settings.password}@{settings.host}:" \
                          f"{settings.port}/{settings.name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base = declarative_base()
