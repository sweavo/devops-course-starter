SH=/bin/bash
PORT=5001

# Makefile to run the app, checking and fixing the environment where 
# possible.

###############################################################################
# entrypoint targets. Users might specify these on the command line

.PHONY: run-flask run-gunicorn-local run-docker test deploy-ansible check choose-board

run-docker: image
	docker run -p ${PORT}:${PORT} todo-app

run-flask: environment
	poetry run flask run --host=0.0.0.0 --port=${PORT} 

run-gunicorn-local: environment
	./with_env.sh poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"

test: environment 
	poetry run pytest

deploy-ansible:
	make -C deploy-ansible

# Check we can start a flask server and connect
check:
	./check-connectivity.sh

# Interactively configure what trello board to use
choose-board:
	poetry run python module-2/exercise/trelloinit.py | tee todo_app/site_trello.json
	@echo "Trello connection data updated on disk.  It's Ok but not necessary to commit the file 'todo_app/site_trello.json'."


###############################################################################
# Internal targets, dependencies of `run`

image:
	docker build --tag todo-app .

environment: poetry-init .env
	@echo "Environment checks complete"

.env: # no dependency, because we don't want to splat a live .env file
	cp .env.template $@

poetry-init:
	if ! which poetry 2>/dev/null; then pip3 install poetry; fi # Install poetry if not present
	poetry install --sync # install any missing deps

all: check choose-board run

