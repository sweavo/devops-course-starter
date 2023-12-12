# Ask flake8 not to complain about unused import.
# It is actually used, but pytest obscures the syntax
import pytest  # noqa: F401; pylint: disable=unused-variable

from todo_app.data import storage_trello
from todo_app.ViewModel import ViewModel


def test_get_done_items():
    """! This tests assumes what persistence layer will return into ViewModel"""
    A, B, C, D = (
        storage_trello.Card(1, "one", "Not Started"),
        storage_trello.Card(2, "two", "Done"),
        storage_trello.Card(3, "three", "Not Started"),
        storage_trello.Card(4, "four", "Done"),
    )

    viewmodel_under_test = ViewModel([A, B, C, D])

    done_items = viewmodel_under_test.done_items

    assert A not in done_items
    assert C not in done_items

    assert B in done_items
    assert D in done_items


def test_get_todo_items():
    """! This tests assumes what persistence layer will return into ViewModel"""
    A, B, C, D = (
        storage_trello.Card(1, "one", "Not Started"),
        storage_trello.Card(2, "two", "Done"),
        storage_trello.Card(3, "three", "Not Started"),
        storage_trello.Card(4, "four", "Done"),
    )

    viewmodel_under_test = ViewModel([A, B, C, D])

    done_items = viewmodel_under_test.todo_items

    assert A in done_items
    assert C in done_items

    assert B not in done_items
    assert D not in done_items
