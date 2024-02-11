SHELL=/bin/bash

include .env

# Default ports for dev and prod runs
# PORT_PROD?=8000 from .env
PORT_DEV?=5000
# External ports default the same as the internal, but if you need to get out of 
# the way of something else on port 5000 you can use `make run-dev PORT_DEV_EXT=5001`
PORT_PROD_EXT?=$(PORT_PROD)
PORT_DEV_EXT?=$(PORT_DEV)

AZ_RES_GRP:=Cohort27_SteCar_ProjectExercise
AZ_SVC_PLAN:=ASP-Cohort27SteCarProjectExercise-8c83
AZ_APP_NAME:=todo-app-SteCar

AZ_ID_APP=--name $(AZ_APP_NAME) --resource-group $(AZ_RES_GRP)

DEFAULT: help

# Makefile to run the app, checking and fixing the environment where 
# possible.

###############################################################################
# entrypoint targets. Users might specify these on the command line

.PHONY: run-flask run-gunicorn-local run-docker test check

# Run the app in a docker image, creating it if needed
run-prod: image-prod
	docker run \
		--env-file .env \
		--publish ${PORT_PROD_EXT}:${PORT_PROD} \
		todo-app:prod ${DOCKER_TAIL}

# Run the app in a docker image in development mode (reloads code on change)
run-dev: image-dev
	docker run \
		--env-file .env \
		--mount type=bind,source="$${PWD}"/todo_app,target=/opt/todoapp/todo_app \
		--publish ${PORT_DEV_EXT}:${PORT_DEV} \
		todo-app:dev ${DOCKER_TAIL}

# Run inside flask
run-native-flask: environment
	poetry run flask run --host=0.0.0.0 --port=${PORT_DEV} 

# Run locally in gunicorn
run-native-gunicorn: environment
	./util/with_env.sh poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"

# Run the unit tests persistently
watch: image-watch
	docker compose run watch

# Run the tests once for CI
test: image-test
	docker compose run test

# Run the feature tests (poking the UI with selenium)
regression-test:
	poetry run ./util/with_dev_server_running.sh ./test_ui.py

# Deploy image to docker, assuming you are logged in with `docker login` already
deploy-docker: image-prod
	docker tag sweavo/todo-app:prod sweavo/todo-app:$$(git rev-parse HEAD)
	docker push sweavo/todo-app:prod
	docker push sweavo/todo-app:$$(git rev-parse HEAD)

# Deploy to azure cloud, creating the service plan
deploy-webapp: deploy-docker az-webapp-variables.json
	az appservice plan create --resource-group $(AZ_RES_GRP) -n $(AZ_SVC_PLAN) --sku B1 --is-linux > az.log
	az webapp create --plan $(AZ_SVC_PLAN) $(AZ_ID_APP) --deployment-container-image-name docker.io/sweavo/todo-app:prod >> az.log
	az webapp config appsettings set $(AZ_ID_APP) --settings @az-webapp-variables.json >> az.log
	@echo Now restart your app...
	az webapp restart $(AZ_ID_APP) >> az.log

# Run the pipeline steps Prepare and Test: check that the pipeline will be able to test
test-pipeline:
	./execute_pipeline_steps.py .github/workflows/build-and-test.yml build Prepare Test

# Print these targets
help:
	@echo "Entrypoints:\n"
	@awk 'BEGIN {a=0} /####/ {a=0} a && /^#/ {line=substr($$0,2)} a && /^[[:graph:]]*:/ {print $$1"\n\t"line"\n"} /.PHONY/ {a=1}' Makefile

# Show the evaluation of a make variable
show:
	$(VAR)="$($(VAR))"

###############################################################################
# Internal targets, dependencies of `run`

# image-dev image-prod and image-test; image-whatever
image-%:
	docker compose build $*

environment: poetry-init .env
	@echo "Environment checks complete"

.env: # no dependency, because we don't want to splat a live .env file
	cp .env.template $@

poetry-init:
	if ! which poetry 2>/dev/null; then pip3 install poetry; fi # Install poetry if not present
	poetry install --sync # install any missing deps

%: %.j2 .env
	poetry run util/j2instantiate.py $< > $@
