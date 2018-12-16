FROM python:3-alpine

WORKDIR /usr/src/app


COPY requirements.txt .


RUN apk add git && \
    pip install -r requirements.txt


COPY . .

CMD [ "python", "./main.py" ]
