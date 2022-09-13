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
To make it work, nedd to change it to **.env**
The folloving variables is used:

- ENV_NAME - it is up to you to have several environment for different purpose ( for ex. Development, QA, Prod)
- BASE_URL - the URL, shortener work on, using [Docker](##Docker) instalation it is localhost
- DB_URL - what a name of a used DB and how it can be found in the app.


## Docker

URL Shortener is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8000, so change this within the
Dockerfile if necessary.


## Tests

write smth here

