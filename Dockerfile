FROM python:3-buster

ENV user_name="app-user"
# requires trello_api_key
# requires trello_token
# requires Install git
# image comes with 2.20.1

# requires Install python 3.x
# image includes Python 3.11.3

# requires create /opt/todoapp with appropriate permissions for app user
RUN mkdir -p /opt/todoapp 

# requires clone to-do app into folder for service
COPY todo_app /opt/todoapp

# requires install poetry
# requires install project dependencies using poetry
# TODO use ansible vault for secrets
# requires configure the systemd service
# requires start the service

EXPOSE 5000
#USER $user_name
CMD ["poetry", "run", "flask", "run"]

# TODO
# use a user not root

