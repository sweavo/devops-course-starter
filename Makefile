SH=/bin/bash

# Makefile to run the flask app, checking and fixing the environment where 
# possible.

###############################################################################
# entrypoint targets. Users might specify these on the command line

# We run flask with --host=0.0.0.0 to support serving on WSL and connecting 
# from Windows.
run: environment
	poetry run flask run --host=0.0.0.0 --port=5001 

# Check we can start a flask server and connect
check:
	./check-connectivity.sh

# Interactively configure what trello board to use
choose-board:
	poetry run python module-2/exercise/trelloinit.py | tee todo_app/site_trello.json
	@echo "Trello connection data updated on disk.  It's Ok but not necessary to commit the file 'todo_app/site_trello.json'."


###############################################################################
# Internal targets, dependencies of `run`

environment: poetry-init .env
	@echo "Environment checks complete"

.env: # no dependency, because we don't want to splat a live .env file
	cp .env.template $@

poetry-init:
	if ! which poetry 2>/dev/null; then pip install poetry; fi # Install poetry if not present
	poetry install --sync # install any missing deps

all: check choose-board run

