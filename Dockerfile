FROM python:latest

ENV HOST 0.0.0.0
ENV PORT 9999

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 9999

RUN pip install redis
RUN pip install gunicorn

