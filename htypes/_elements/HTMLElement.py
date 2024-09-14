"""
Base class for all elements
"""

from typing import List, Union, Optional

class HTMLElement:
    def __init__(
        self,
        tag: str,
        attributes: Optional[dict] = None,
        children: Optional[List[Union['HTMLElement', str]]] = None,
        text: Optional[str] = None
    ):
        self.tag = tag
        self.attributes = attributes or {}
        self.children = children or []
        self.text = text or None

    def __repr__(self):
        return f"HTMLElement(tag='{self.tag}', attributes={self.attributes}, children={self.children}, text='{self.text}')"
    
    def to_dict(self) -> dict:
        """Converts the HTMLElement and its children to a dictionary representation."""
        return {
            "tag": self.tag,
            "attributes": self.attributes,
            "children": [
                child.to_dict() if isinstance(child, HTMLElement) else child
                for child in self.children
            ],
            "text": self.text
        }