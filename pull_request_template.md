# Project exercise submission for module __

## README

- [ ] Explains steps required to set up the app
- [ ] Any new environment variables have placeholders in the .env.template file
- [ ] Anyone could run the app following the README instructions
- [ ] Explains how to run the tests
- [ ] Explains how to build and run development and production containers
- [ ] Explains how to run the docker tests
- [ ] Explains how to mount your project in the development container so that flask automatically reloads when you edit your Python files

## Secrets

- [ ] No secrets are included in the built images (check the diff and run `submission_check.sh`)

## App

- [ ] You can create a new to-do item and see it immediately appear on the page (regression test)

## Tech debt

- [ ] the code passed pyflakes linting
- [ ] You’ve deleted any unused or commented out code - it’ll be in your git history if you need it

## Test

- [ ] There is at least one unit test and at least one integration test
- [ ] New unit tests each test one file/class and nothing else, without depending on their environment
- [ ] New integration tests use mocking to avoid making external requests, and don’t have access to real credentials
- [ ] New e2e tests load real credentials and perform some browser interaction resulting in requests to database
- [ ] All new tests test something meaningful - they should probably all contain at least one assert
- [ ] Tests can be successfully run outside of IDE by pytest or `poetry run pytest path/to/test_file`

## Docker

- [ ] A single, multi-stage Dockerfile is used to specify development and production containers
- [ ] Production containers uses a production-ready server (gunicorn) to run the app

## Pipeline

- [ ] Does the pipeline run on push and on pull request
- [ ] Does the pipeline run all the tests
