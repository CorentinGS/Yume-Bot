FROM gorialis/discord.py:rewrite

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY . .

CMD [ "python", "./main.py" ]
CMD [ "python", "./api/rest.py" ]
