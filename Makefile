SH=/bin/bash

# Makefile to remind me that I need to specify --host if I'm running in WSL and browsing from Windows.
#
run: environment
	poetry run flask run --host=0.0.0.0

test:
	./test.sh


environment: poetry-init .env
	@echo "Envrionment checks complete"

.env: .env.template
	cp $^ $@

poetry-init:
	if ! which poetry 2>/dev/null; then pip install poetry; fi # Install poetry if not present
	poetry install --sync # install any missing deps
