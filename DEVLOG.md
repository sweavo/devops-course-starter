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
* `[X]` util/TrelloSession.py
* `[X]` util/trelloinit.py
* `[X]` todo_app/data/TrelloSession.py
* `[X]` todo_app/data/storage_trello.py 

### Likely to change as part of the work
* `[X]` todo_app/data/storage_mongo.py
* `[ ]` az-webapp-variables.json.j2
* `[ ]` tests/integration_test.py
* `[ ]` util/with_env.sh
* `[ ]` expected.subcheck

### Review at end
* `[ ]` tests/test_data/board_result.json
    - still needed after integration test change?
* `[ ]` Makefile
* `[ ]` README.md
* `[ ]` architecture/c4-0.svg
* `[ ]` architecture/c4-1.svg
* `[ ]` architecture/c4-2.svg
* `[ ]` pull_request_template.md

I'll come back here and check them off as I do them, and put them on the backlog below.

### todo_app/data/storage_mongo.py - rewrite for mongo



## BACKLOG


* ex10: unit tests?
* ex10: integration tests?
* ex10: e2e tests?

* update the app to be able to spin up using a clean or predetermined test database
* consider whether pytest can be used here too, using setup to start the test server instance
* use the page object pattern



