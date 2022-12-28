SH=/bin/bash

# Makefile to remind me that I need to specify --host if I'm running in WSL and browsing from Windows.
#
run:
	poetry run flask run --host=0.0.0.0

test:
	./test.sh
