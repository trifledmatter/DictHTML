from typing import List
from .HTMLElement import HTMLElement

class HTMLHeadElement(HTMLElement):
    def __init__(
        self,
        attributes: dict | None = None,
        children: List[HTMLElement | str] | None = None,
    ):
        super().__init__('head', attributes, children)

    def __repr__(self):
        return f"HTMLHeadElement(tag='{self.tag}', attributes={self.attributes}, children={self.children}, text='{self.text}')"