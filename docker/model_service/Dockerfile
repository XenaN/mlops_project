FROM python:3.9

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry
RUN file="$(ls -1 ./)" && echo $file

COPY ./pyproject.toml ./poetry.lock /code/
COPY ./src/app /code/app

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
  
CMD ["uvicorn", "app.inference:app", "--host", "0.0.0.0", "--port", "80"]

