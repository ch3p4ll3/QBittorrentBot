FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV IS_DOCKER True

COPY . .

VOLUME [ "/app/config" ]

CMD [ "python3", "-u", "./main.py"]
