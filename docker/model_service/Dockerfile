FROM python:3.9

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /code/
COPY ../../src/app /code/app
COPY ./.env code/app/.env

RUN poetry config virtualvenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi
  
 CMD ["unicorn", "app.inference:app", "--host", "0.0.0.0", "--port", "80"]