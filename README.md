# URL Shortener API

Pet project: URL Shortener app that allows to customise links and make it shorter and convenient to use.
Using FastApi, uvicorn as a server, loguru for logs and pytest for unit tests.

Endpoints for the API provided bellow:

| Endpoint | HTTP Verb | Request Body | Action | 
| -------- | --------- | ------------ | ------ |
| / | GET | - | Hello, welcome to the URL shortener API |
| /url | POST | Your target URL | Shows the created url_key with additional info, including a secret_key |
| /{url_key} | GET | - | Forwards to your target URL |
| /admin/{secret_key} | GET | - | Shows administrative info about your shortened URL |
| /admin/{secret_key} | DELETE | Your secret key | Deactivate your shortened URL | 


## Features

- Generate short key to modify a long URL
- Count how many times an endpoint is visited
- Deactivate a URL if it is no needed


## Requirements

All sources that should be installed is in requirements.txt file.
To have it installed independently, the following command should be run:

```pip install requirements.txt```


## Configuration

All environment variable, that the project uses is in .env file ( It is insecure to store it open, so you can find a sample, called ***.env_sample***
To make it work, need to change it to **.env** and add your data there
The following variables is used:

- **ENV_NAME** - it is up to you to have several environment for different purpose ( for ex. Development, QA, Prod)
- **BASE_URL** - the URL, shortener work on, using [Docker](##Docker) instalation it is localhost
- **DB_URL** - what a name of a used DB and how it can be found in the app.
- **DB_USERNAME** - username for your database
- **DB_PASSWORD** - password for enter the DB
- **DB_NAME** - name of your database
- **DB_HOST** - the host where your DB is running
- **DB_PORT** - The DB port

## Run Application

To have the API running without docker file:

- Clone the project
- Change .env_sample to .env
- Change data in .env
- Go to project folder and run : 
 ```uvicorn shortener/main:app --reload ```

## Docker

URL Shortener is very easy to install and deploy in a Docker container.

PostgreSQL is used as a separate container, so to make application up and running:

```
docker-compose up -d
```

To have the application running :
```
docker exec 7c5431217444  uvicorn main:app --reload
```

To connect to the PostgreSQL:
``
docker-compose exec db psql --username=postgres --dbname=shortener_db
```



## Tests

Tests can be run from Python Console using: 
```python -m pytest test_main.py```

To run a particular case use:

```pytest test_main.py::[put_func_name_here]```


