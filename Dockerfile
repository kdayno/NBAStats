FROM python:3.9-slim

RUN mkdir app
WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./

CMD gunicorn -b 0.0.0.0:80 --chdir src app:server