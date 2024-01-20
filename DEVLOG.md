# Dev log

## 2024-01-20 Found a bug!

Given n open items and some closed items.  If you click closed item i and i < n then open item i gets closed rather than closed item i getting opened.  This looks likely because the form names are re-used, form1 form2 etc., for each set of items (open, closed respectively).

The experiment and fix looks easy, but what does the test look like? Selenium?

Installed selenium in poetry under group "test" (also dev, erroneously) and got chromedriver from the web.  But it doesn't work, I guess because linux's chromedriver can't start windows' chrome.

To try next: just execute the test in powershell instead of wsl bash.



