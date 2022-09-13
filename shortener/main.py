import logging
from pathlib import Path

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

from .config import get_settings
from .custom_logging import CustomizeLogger
from .database import SessionLocal, engine

from shortener import schemas, models, crud

#  Initialize logger
logger = logging.getLogger(__name__)

#  Set up logs view
config_path = Path(__file__).with_name("logging_config.json")


def create_app() -> FastAPI:
    """
    Define FastAPI application with initialized logger
    :return: application Object
    """
    app = FastAPI(title='URL Shortener', debug=False)
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app


#  Create app using function create_app()
app = create_app()

#  Bind the database engine with models
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Create and yield new database sessions with each request
    :return: DB session (Object)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message):
    """
    Helper function. Raise a custom message with 400 status code
    :param message: String parameter to notify user
    :return: Exception instance with a custom message
    """
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    """
    Helper function. Raise 404 status code if the provided URL.key does not match any URLs in the DB
    :param request: URL is reaching
    :return: 404 exception instance with detail
    """
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    """
    Show the admin information like clicks and active status
    :param db_url: Db instance with secret_key
    :return: DB instance with a short_key and a secret_key
    """
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.short_key_to_url))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.get("/")
def index_page():
    """
    Intro function
    :return: Greetings info
    """
    return "Hello, welcome to the URL shortener API"


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
    Send the POST request to API endpoint and get responses in return
    :param url: String URL as a POST request body
    :param db: DB instance for current session
    :return: A DB url record
    """
    if not validators.url(url.original_url):
        raise_bad_request(message="Your provided URL is not valid")

    db_url = crud.create_url_record_to_db(db=db, url=url)
    return get_admin_info(db_url)


@app.get("/{url_short_key}")
def forward_to_original_url(
        url_short_key: str,
        request: Request,
        db: Session = Depends(get_db)
):
    """
    Perform redirect using short URL
    :param url_short_key: Generated key, in addition to the local host lead to origin URL
    :param request: URL is reaching with /{url_short_key} endpoint
    :param db: DB instance for current session
    :return: 200 status code and instance of RedirectResponse
    """

    if db_url := crud.get_db_url_by_short_key(db=db, url_key=url_short_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.original_url)
    else:
        raise_not_found(request)


@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo,
)
def get_url_info(
        secret_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    To show the statistic for a user with secret_key
    :param secret_key: DB value can be provided to manage shortened URL and see statistics(like clicks)
    :param request: URL is reaching with /admin/{secret_key} endpoint
    :param db: DB instance for current session
    :return: DB records with info for sent secret_key
    """
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)


@app.delete("/admin/{secret_key}")
def delete_url(
        secret_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    Deactivate DB record,setting is_active to False
    :param secret_key: Admin info key that is generated with short link
    :param request: URL is reaching with /admin/{secret_key} endpoint
    :param db: DB instance for current session
    :return: Success message with an original link is deactivated or 404 in case record is not in DB
    """
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.original_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)
