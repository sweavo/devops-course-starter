# Dev log

## 2024-01-20 Found a bug!

Given n open items and some closed items.  If you click closed item i and i < n then open item i gets closed rather than closed item i getting opened.  This looks likely because the form names are re-used, form1 form2 etc., for each set of items (open, closed respectively).

The experiment and fix looks easy, but what does the test look like? Selenium?

Installed selenium in poetry under group "test" (also dev, erroneously) and got chromedriver from the web.  But it doesn't work, I guess because linux's chromedriver can't start windows' chrome.

To try next: just execute the test in powershell instead of wsl bash.

## 2024-02-11 Got a regression test

By installing chromium-chromedriver in WSL, I don't have to worry about cross-platform webdriver stuff.  Now I have one working test.  Before getting very far with such tests, I would need to restructure the tests.

Exercise 10:

Here are the files that mention trello:

### Leave as-is, part of trello backend
* `[X] util/TrelloSession.py`
* `[X] util/trelloinit.py`
* `[X] todo_app/data/TrelloSession.py`
* `[X] todo_app/data/storage_trello.py `

### Likely to change as part of the work
* `[X] todo_app/data/storage_mongo.py`
* `[X] az-webapp-variables.json.j2`
* `[X] tests/integration_test.py`
* `[X] util/with_env.sh`
* `[X] expected.subcheck`

### Review at end
* `[X] tests/test_data/board_result.json`
    - still needed after integration test change?
        - nope, removed
* `[X] Makefile`
* `[X] README.md`
* `[X] architecture/c4-0.svg`
* `[X] architecture/c4-1.svg`
* `[X] architecture/c4-2.svg`
* `[X] pull_request_template.md`

I'll come back here and check them off as I do them, and put them on the backlog below.

### todo_app/data/storage_mongo.py - rewrite for mongo

I have to be careful not to instantiate the database on import of the storage module, or there is no time to get in with any mocking.

This is done; and it was cathartic to remove a lot of noise in there to handle trello, its authentication, the hacky way we stored statuses in there, etc.


## BACKLOG

* use pytest for the e2e test, using setup to start the test server instance
* update the app to be able to spin up using a clean or predetermined test database
* use the page object pattern in selenium tests
* The Card object is neither an interface nor an implementation. Refactor.



