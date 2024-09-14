from typing import List
from .HTMLElement import HTMLElement

class HTMLHeadElement(HTMLElement):
    def __init__(
        self,
        attributes: dict | None = None,
        children: List[HTMLElement | str] | None = None,
    ):
        super().__init__('head', attributes, children)