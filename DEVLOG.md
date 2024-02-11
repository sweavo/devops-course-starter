# Dev log

## 2024-01-20 Found a bug!

Given n open items and some closed items.  If you click closed item i and i < n then open item i gets closed rather than closed item i getting opened.  This looks likely because the form names are re-used, form1 form2 etc., for each set of items (open, closed respectively).

The experiment and fix looks easy, but what does the test look like? Selenium?

Installed selenium in poetry under group "test" (also dev, erroneously) and got chromedriver from the web.  But it doesn't work, I guess because linux's chromedriver can't start windows' chrome.

To try next: just execute the test in powershell instead of wsl bash.

## 2024-02-11 Got a regression test

By installing chromium-chromedriver in WSL, I don't have to worry about cross-platform webdriver stuff.  Now I have one working test.  Before getting very far with such tests, I would need to restructure the tests.

## BACKLOG

* update the app to be able to spin up using a clean or predetermined test database
* consider whether pytest can be used here too, using setup to start the test server instance
* use the page object pattern



