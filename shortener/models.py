# The module describes the contention of a database and declare how data should be stored there

from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, index=True)
    short_key_to_url = Column(String, unique=True, index=True)  # A random string that’ll be part of the shortened URL
    secret_key = Column(String, unique=True, index=True)  # A value is for managing shortened URL for users
    is_active = Column(Boolean, default=True)  # Flag that helps to deactivate (not delete) instance of a short URL
    clicks = Column(Integer, default=0)  # Count a short link visits

    def __repr__(self):
        return "<URL(original_url='{}', short_key_to_url='{}', secret_key={}, is_active={}, clicks={})>"\
                .format(self.original_url, self.short_key_to_url, self.secret_key, self.is_active, self.clicks)
