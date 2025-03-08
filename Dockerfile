FROM python:3.11.7-alpine

COPY . .

RUN apk add --virtual .build-deps gcc musl-dev \
    && pip install -r ./requirements.txt \
    && apk del .build-deps

EXPOSE 5000