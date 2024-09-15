from parser import *
from typing import Union, List


class HTMLRenderer:
    def __init__(self, indent: bool = False):
        """
        :param indent: If True, the renderer will pretty print the HTML with indentation.
        """
        self.indent = indent
        self.current_indent = 0

    def render(self, element: Union[HTMLElement, HTMLPlainText], level: int = 0) -> str:
        """
        Renders an HTMLElement or HTMLPlainText back into HTML.
        :param element: The root element to render.
        :param level: Current depth for indentation purposes.
        :return: A string containing the HTML.
        """
        if isinstance(element, HTMLPlainText):
            return self.render_text(element)

        tag = element.tag
        attributes = self.render_attributes(element.attributes)
        children = self.render_children(element.children, level + 1)

        if tag in ["br", "img", "input", "meta", "link", "hr"]:
            return self.render_self_closing_tag(tag, attributes)

        opening_tag = f"<{tag}{attributes}>"
        closing_tag = f"</{tag}>"

        if self.indent:
            indent_space = "    " * level
            children = f"\n{children}\n" if children else ""
            return f"{indent_space}{opening_tag}{children}{indent_space}{closing_tag}"
        else:
            return f"{opening_tag}{children}{closing_tag}"

    def render_text(self, text_node: HTMLPlainText) -> str:
        """Renders a text node."""
        if self.indent:
            return text_node.text.strip()
        return text_node.text

    def render_attributes(self, attributes: dict) -> str:
        """Converts attributes dict into a string like ` class="container" id="main"`."""
        if not attributes:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in attributes.items())

    def render_children(
        self, children: List[Union[HTMLElement, str]], level: int
    ) -> str:
        """Recursively renders the children of an element."""
        if not children:
            return ""
        rendered_children = [self.render(child, level) for child in children]
        if self.indent:
            return "\n".join(rendered_children)
        return "".join(rendered_children)

    def render_self_closing_tag(self, tag: str, attributes: str) -> str:
        """Renders self-closing tags like <br />, <img />, etc."""
        if self.indent:
            return f"<{tag}{attributes} />"
        return f"<{tag}{attributes}/>"
