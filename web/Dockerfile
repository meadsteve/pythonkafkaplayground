FROM python:3.7.0

WORKDIR /app

RUN pip install pipenv

COPY Pipfile /app
COPY Pipfile.lock /app

RUN pipenv install --deploy --system

COPY djangfa /app/

EXPOSE 8000

CMD ./manage.py runserver 0.0.0.0:8000