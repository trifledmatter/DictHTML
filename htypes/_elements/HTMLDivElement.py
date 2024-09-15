from typing import List
from .HTMLElement import HTMLElement

class HTMLDivElement(HTMLElement):
    def __init__(
        self,
        attributes: dict | None = None,
        children: List[HTMLElement | str] | None = None,
    ):
        super().__init__('div', attributes, children)
    
    def __repr__(self):
        return f"HTMLDivElement(tag='{self.tag}', attributes={self.attributes}, children={self.children}, text='{self.text}')"