#!/bin/env python3
""" Regression test for the bug where unchecking a done item doesn't always result in setting it to open.

    Analysis: when you have an open item and a done item and you click the `i`th done item,
    it results in checking the `i`th open item, not unchecking the `i`th done item.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("http://localhost:5000")

list_group = driver.find_element(By.CLASS_NAME, "list-group")
list_items = list_group.find_elements(By.TAG_NAME, "li")

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
        "Test cannot run: need at least one open and one closed item in the test data"
    )

print("click")
toggle.click()

# refresh the DOM
list_group = WebDriverWait(driver, 4).until(
    EC.presence_of_element_located((By.CLASS_NAME, "list-group"))
)
list_item = list_group.find_element(By.ID, item_id)

toggle = list_item.find_element(By.TAG_NAME, "input")
if toggle.is_selected():
    raise SystemError(
        f'Test Fail: clearing the done flag of {item_id} "{list_item.text}" did not result in it transitioning'
    )
else:
    print("test PASS")
    toggle.click()
