FROM python:3-slim-buster as base

ENV user_name="app-user"

# requires python 3.x
# image includes Python 3.11.3

# requires poetry
RUN pip3 install poetry

# requires /opt/todoapp with appropriate permissions for app user
RUN mkdir -p /opt/todoapp/todo_app

# requires to-do app in folder for service
COPY todo_app /opt/todoapp/todo_app

# requires project dependencies via poetry
COPY poetry.lock /opt/todoapp
COPY pyproject.toml /opt/todoapp
WORKDIR /opt/todoapp
RUN poetry install


FROM base as prod

    EXPOSE 8000
    CMD ["poetry", "run", "gunicorn", "--bind=0.0.0.0", "todo_app.app:create_app()"]


FROM base as dev

    VOLUME /opt/todoapp

    EXPOSE 5000
    CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]
