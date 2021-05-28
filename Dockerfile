FROM python:3.9.5-buster

ENV FLASK_ENV=production

WORKDIR .

COPY ./requirements.txt requirements.txt

RUN python3.9 -m pip install -U pip

RUN python3.9 -m pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]

CMD  python3.9 app.py