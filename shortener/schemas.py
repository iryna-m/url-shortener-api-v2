# The module defines what data the API expected from a client and the server

from pydantic import BaseModel


class URLBase(BaseModel):
    original_url: str


class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class URLInfo(URL):
    url: str
    admin_url: str