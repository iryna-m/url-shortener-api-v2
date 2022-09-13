# Contain helper functions that generate key and secret_key for short_url

import secrets
import string

from sqlalchemy.orm import Session

from shortener import crud


def create_random_short_key(length: int = 5) -> str:
    """
    Generate random key with dfault length = 5
    :param length: The desirable length of a key
    :return: String variable that contains generated key
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    """
    Generate and check the key for uniqueness
    :param db: DB object for current session
    :return: Unique short_key, type string
    """
    short_key = create_random_short_key()
    while crud.get_db_url_by_short_key(db, short_key):
        short_key = create_random_short_key()
    return short_key
