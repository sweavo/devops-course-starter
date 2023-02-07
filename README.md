# DevOps Apprenticeship: Project Exercise

## System Requirements

You need python 3.7+, poetry, and some local configuration.  If you are using `bash` and have a working `make` then just issue

    $ make
    
... and it will attempt most of the setup and initialization for you.  On your first run it will fail to authenticate against trello and you then need to provide your credentials in the `.env` file.

If you don't have `bash` and `make`, or if this didn't work, then the manual steps are listed below.

## Trello Setup

If using the trello persistence layer, you need to configure trello in a particular way:

1. Create a board (any name) with at least one list called "Not Started".
2. Create an integration via the powerups pages at https://trello.com/power-ups/admin that can access that board
3. Note your API Key and your Token as you will need them for _Credentials_ below (follow the hyperlink next to the API key in the powerup admin pages)

## Credentials

To run the app you need a `.env` file containing at least `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY`, `TRELLO_API_KEY`, and `TRELLO_TOKEN`.  The `Makefile` will create this if it doesn't exist. 

The `FLASK`* values are fine to leave as they are, but the `TRELLO_` values need to be initialized with your API key and Token from _Trello Setup_ above.  Just paste the keys after the equals signs, no quotes.

There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Find the board's ID

Once you have the `TRELLO_API_KEY` and `TRELLO_TOKEN` set up, you can try

```bash
$ make choose-board
```

This lists the boards that you were authorised to see, and asks you to choose one, then writes the config to the app. You see something like the following:

```bash
poetry run python module-2/exercise/trelloinit.py | tee todo_app/trello_config.py
Connect OK.
 0: Refinement: Cost
 1: corndel
Choose: 1
... json ...
Trello connection data updated on disk.  It's Ok but not necessary to commit the file.
```

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ make
```

You should see output similar to the following:
```bash
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



# GitPod

If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.