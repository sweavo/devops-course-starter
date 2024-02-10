#!/bin/env python3
""" Regression test for the bug where unchecking a done item doesn't always result in setting it to open.

    Analysis: when you have an open item and a done item and you click the `i`th done item,
    it results in checking the `i`th open item, not unchecking the `i`th done item.

    The test looks through the list items in list-group, getting the first closed item found.

    If it achieves this without seeing any open items, then it's a precondition failure.


    ISSUE1: there is no clean room for the test, it runs on the "live" data so might fail its
            precondition check, and might leave mess in the data.

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Get the page and grab the todo items

driver.get("http://localhost:5000")

list_group = driver.find_element(By.CLASS_NAME, "list-group")
list_items = list_group.find_elements(By.TAG_NAME, "li")


# GIVEN some open todo item and a closed todo item

seen_input = False
seen_open_items = False
found_closed_item = False

for i, list_item in enumerate(list_items):
    item_id = list_item.get_attribute("id")
    toggle = list_item.find_element(By.TAG_NAME, "input")
    if toggle.is_selected():
        found_closed_item = True
        break
    else:
        seen_open_items = True

if seen_open_items and found_closed_item:
    print(f"test can be valid: {item_id} is the first closed item")
else:
    raise SystemExit(
        "PRECONDITION FAIL: need at least one open and one closed item in the test data"  # see ISSUE1
    )

# WHEN I click the closed todo item's toggle button

toggle.click()

# - The click caused a form submit, so reorient in the DOM
list_group = WebDriverWait(driver, 4).until(
    EC.presence_of_element_located((By.CLASS_NAME, "list-group"))
)
list_item = list_group.find_element(By.ID, item_id)
toggle = list_item.find_element(By.TAG_NAME, "input")

# THEN the item's status is reset to open
if toggle.is_selected():
    raise SystemError(
        f'Test Fail: clearing the done flag of {item_id} "{list_item.text}" did not result in it transitioning'
    )
else:
    print("test PASS")
    # - Put the status back how we found it (see ISSUE1)
    toggle.click()
