FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./


RUN apk update && \
    apk upgrade && \
    apk add git && \
    pip install -U -r requirements.txt


COPY . .

CMD [ "python", "./main.py" ]
