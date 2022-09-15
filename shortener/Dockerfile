FROM python:3.8.3-slim

# set working directory
WORKDIR /shortener

# set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project to Docker working directory
COPY requirements.txt /shortener/requirements.txt
COPY . .

# set dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"]
