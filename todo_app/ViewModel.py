"""ViewModel

Making a Model-View-Controller architecture so that there are seam for
testing the business objects.
"""


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items
