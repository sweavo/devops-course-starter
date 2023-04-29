# DevOps Apprenticeship: Project Exercise

## System Requirements

You need python 3.7+, poetry, and some local configuration.  If you are using `bash` and have a working `make` then just issue

    $ make
    
... and it will attempt most of the setup and initialization for you.  On your first run it will fail to authenticate against trello and you then need to provide your credentials in the `.env` file.

If you don't have `bash` and `make`, or if this didn't work, then the manual steps are listed below.

### python conflict

The deployment target has no python after 3.7.11, but the commit hooks for flake8 and black need a later python than 3.8.  So I took out all the poetry declarations of flake8 and so on.  So you have to keep your python tidy by yourself again.

## Trello Setup

The app uses trello for its backend.  So you need to configure trello in a particular way:

1. Create a board (any name) with at least one list called "Not Started".
2. Create an integration via the powerups pages at https://trello.com/power-ups/admin that can access that board
3. Note your API Key and your Token as you will need them for _Credentials_ below (follow the hyperlink next to the API key in the powerup admin pages)

## Credentials

To run the app you need a `.env` file containing at least `FLASK_APP`, `FLASK_DEBUG`, `SECRET_KEY`, `TRELLO_API_KEY`, and `TRELLO_TOKEN`.  The `Makefile` will create this if it doesn't exist. 

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

There is a file committed that connects to my board, for the deployment exercise

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


## Developing

Testing is done via pytest, and there is a Make recipe too.

```bash
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
```


## Deploy

You need ansible >2.11.

If you are using WSL2/ubuntu20.04 as your control node, you need to add a package source to get access to more modern ansible than 2.9.

```
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt install ansible
```

As you may expect by now, the _how_ of deployment is captured in `make` recipies.

```
$ make deploy
```

This will deploy using the credentials you put in the `.env` file during _Credentials_ above.  The Makefile will quit the deployment if they are not successfully read.

