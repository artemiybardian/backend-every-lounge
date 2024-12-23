FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip setuptools

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

