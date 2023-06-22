SHELL=/bin/bash
PORT_PROD=8000
PORT_DEV=5000

DEFAULT: help

# Makefile to run the app, checking and fixing the environment where 
# possible.

###############################################################################
# entrypoint targets. Users might specify these on the command line

.PHONY: run-flask run-gunicorn-local run-docker test check choose-board

# Run the app in a docker image, creating it if needed
run-prod: image-prod
	# See git history for how to run without compose
	docker compose run prod ${DOCKER_TAIL}

run-dev: image-dev
	# See git history for how to run without compose
	docker compose run dev ${DOCKER_TAIL}

# Run inside flask
run-native-flask: environment
	poetry run flask run --host=0.0.0.0 --port=${PORT_DEV} 

# Run locally in gunicorn
run-native-gunicorn: environment
	./util/with_env.sh poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"

# Run the unit tests
test: environment 
	poetry run pytest

# Interactively configure what trello board to use
choose-board:
	set -o pipefail; poetry run python util/trelloinit.py | tee todo_app/site_trello.json
	@echo "Trello connection data updated on disk.  It's Ok but not necessary to commit the file 'todo_app/site_trello.json'."

# Print these targets
help:
	@echo "Entrypoints:\n"
	@awk 'BEGIN {a=0} /####/ {a=0} a && /^#/ {line=substr($$0,2)} a && /^[[:graph:]]*:/ {print $$1"\n\t"line"\n"} /.PHONY/ {a=1}' Makefile

###############################################################################
# Internal targets, dependencies of `run`

image-prod:
	docker compose build prod

image-dev:
	docker compose build dev

environment: poetry-init .env
	@echo "Environment checks complete"

.env: # no dependency, because we don't want to splat a live .env file
	cp .env.template $@

poetry-init:
	if ! which poetry 2>/dev/null; then pip3 install poetry; fi # Install poetry if not present
	poetry install --sync # install any missing deps
