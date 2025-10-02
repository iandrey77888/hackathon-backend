FROM python:3.12

RUN mkdir /code

COPY . /code

RUN pip install -r /code/requirements-linux.txt

ENV DB_URL=postgresql+psycopg2://DB_USER:DB_PWD@kontorskii-backend-db-1:5432/ecmkontorskii

WORKDIR /code

ENTRYPOINT ["gunicorn", "main:app", "-w 4", "-k uvicorn.workers.UvicornWorker", "-b 0.0.0.0:8002" ]