a change to test commithook
# DevOps Apprenticeship: Project Exercise

## Todo App

&rarr; Find it here:  [Todo app](https://todo-app-stecar.azurewebsites.net/)


## System Requirements

You need python 3.7+, poetry, and some local configuration.  If you are using `bash` and have a working `make` then just issue

    $ make environment
    
... and it will attempt most of the setup and initialization for you.  

All permutations of { docker, native } X { flask X gunicorn } can be attempted, to see what maketargets are supported, type 

    $ make

For example, to run development server without docker, try:

    $ make run-native-flask

On your first run it will fail to authenticate against mongodb and you then need to provide your connection string in the `.env` file.

If you don't have `bash` and `make`, or if this didn't work, then the manual steps are listed below.


## Database Setup

Use the `MONGODB_URI` variable in .env to provide your connection string.  There is no other setup needed, since mongo itself lazily creates anything requested by the app.

## Credentials

To run the app you need a `.env` file containing at least `FLASK_APP`, `FLASK_DEBUG`, `SECRET_KEY`, and `MONGODB_URI`.  The `Makefile` will create this if it doesn't exist. 

The `FLASK*` values are fine to leave as they are, but the `MONGODB_URI` value need to be initialized with your connection string.  Just paste the keys after the equals signs, no quotes.

There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:

    $ make run-native-flask

You should see output similar to the following:

    if ! which poetry 2>/dev/null; then pip install poetry; fi # Install poetry if not present
    .../.local/bin/poetry
    poetry install --sync # install any missing deps
    Installing dependencies from lock file

    No dependencies to install or update

    Installing the current project: todo-app (0.1.0)
    Environment checks complete
    * Serving Flask app "app" (lazy loading)
    * Environment: development
    * Debug mode: on
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with fsevents reloader
    * Debugger is active!
    * Debugger PIN: 226-556-590
    ```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Developing

Testing is done via pytest, and there is a Make recipe too.

    $ make test
    if ! which poetry 2>/dev/null; then pip install poetry; fi # Install poetry if not present
    /c/Users/crs1yok/AppData/Local/Programs/Python/Python311/Scripts/poetry.exe
    poetry install --sync # install any missing deps
    Installing dependencies from lock file

    No dependencies to install or update

    Installing the current project: todo-app (0.1.0)
    Environment checks complete
    poetry run pytest
    ============================= test session starts =============================
    platform win32 -- Python 3.11.2, pytest-7.2.2, pluggy-1.0.0
    rootdir: c:\Users\crs1yok\Documents\Source\devops-course-starter, configfile: pytest.ini, testpaths: tests
    collected 2 items

    tests\test_view_model.py ..                                              [100%]

    ============================== 2 passed in 0.44s ==============================

There's also a docker container and github workflow for testing, and you can invoke that with 

    $ make test-pipeline

## Regression Tests

Since finding a bug that could not be sensibly automated in pytest, regression testing is via selenium chromedriver.  Setup depends on your OS; for WSL Ubuntu, you can 

    $ sudo apt install --upgrade chromium-chromedriver

Worst case, you can install chrome, then download and drop chromedriver binary in the `tests/` folder. Then, to run the test, use

    $ make regression-test

**NOTE** the regressions tests operate on the live data, which is only OK because this whole app is an exercise :-)

## Deploy

The following steps are all done by github actions on pushing to `main`.  If you want to execute the deployment manually, issue 

    $ make deploy-webapp

Follow the Makefile dependencies to see what happens as a result.  

The environment variables passed to the deployed app are set in `az-webapp-variables.json` which is generated by jinja2.

When done manually, you will need to go to portal.azure.com and restart the app.  When done by github actions, the action calls a webhook to do this (recorded as a secret in the repo)
