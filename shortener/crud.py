# The module contains functions to cover CRUD operations in database

from sqlalchemy.orm import Session

import keygen, models, schemas


def get_db_url_by_short_key(db: Session, url_key: str) -> models.URL:
    """
    Tells if a key exists in DB
    :param db: DB object for current session
    :param url_key: key is to search for in DB
    :return: Either None or a database entry with a provided key
    """
    return (
        db.query(models.URL)
        .filter(models.URL.short_key_to_url == url_key, models.URL.is_active)
        .first()
    )


def create_url_record_to_db(db: Session, url: schemas.URLBase) -> models.URL:
    """
    Create record in DB with created short_key
    :param db: DB object for current session
    :param url: parameters that should be validated and updated in DB
    :return: A record in the DB with new short key
    """
    short_key_to_url = keygen.create_unique_random_key(db)
    secret_key = f"{short_key_to_url}_{keygen.create_random_short_key(length=8)}"
    db_url = models.URL(
        original_url=url.original_url, short_key_to_url=short_key_to_url, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Checks your database for an active database entry with the provided secret_key
    :param db: DB object for current session
    :param secret_key: DB value can be provided to manage shortened URL and see statistics(like clicks)
    :return: If a database entry is found, then it returns the entry. Otherwise, you return None
    """
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    """
    Count the clicks when shortened URL is visited
    :param db: DB object for current session
    :param db_url: An existing database entry
    :return: A number of time the link is visited
    """
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    """
    Deactivate short URL (not Delete) in case it can be recovered by admin
    :param db: DB object for current session
    :param secret_key: A short_key value that exists in DB
    :return: The success message. Otherwise, 404
    """
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
