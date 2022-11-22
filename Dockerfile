FROM python:3.11.0-slim-bullseye

WORKDIR /moniker

# Install and configure Poetry
# https://github.com/python-poetry/poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Install dependencies
COPY pyproject.toml pyproject.toml
RUN poetry install

COPY . .

CMD [ "python", "moniker.py" ]
