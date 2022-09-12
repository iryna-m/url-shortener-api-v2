# The module describes the contention of a database and declare how data should be stored there

from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    short_key_to_url = Column(String, unique=True, index=True)  # A random string that’ll be part of the shortened URL
    secret_key = Column(String, unique=True, index=True)  # A value is for managing shortened URL for users
    original_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)