from typing import List
from .HTMLElement import HTMLElement

class HTMLPlainText(HTMLElement):
    """
    This will be used to classify text with no designated text-related parent element.
    Will classify as a <span> by default.
    """
    def __init__(self, attributes: dict | None = None, children: List[HTMLElement | str] | None = None):
        super().__init__('span', attributes, children)