import secrets
import string

from sqlalchemy.orm import Session

from shortener import crud


def create_random_short_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    short_key = create_random_short_key()
    while crud.get_db_url_by_short_key(db, short_key):
        short_key = create_random_short_key()
    return short_key
