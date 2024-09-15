import re
from tokenizer import HTMLTokenizer
from htypes import HTMLElement, HTMLHeadElement, HTMLBodyElement, HTMLDivElement, HTMLLinkElement, HTMLPlainText

class HTMLParser:
    def __init__(self, html: str):
        self.tokenizer = HTMLTokenizer(html)
        self.root = None
        self.text_related_elements = {"title", "p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "a", "div", "body"}

    def parse(self) -> HTMLElement:
        """Starts parsing and returns the root element of the parsed HTML tree."""
        elements_stack = []
        current_element = None

        while True:
            token = self.tokenizer.next_token()
            if token is None:
                break

            if token.startswith("</"):
                if elements_stack:
                    finished_element = elements_stack.pop()
                    if elements_stack:
                        elements_stack[-1].children.append(finished_element)
                    else:
                        current_element = finished_element

            elif token.startswith("<"):
                tag_name, attributes = self.parse_tag(token)
                element = self.classify_element(tag_name, attributes)
                # print(element)

                if tag_name in ["br", "img", "input", "meta", "link", "hr"]:
                    if elements_stack:
                        elements_stack[-1].children.append(element)
                else:
                    elements_stack.append(element)

            else:
                text = token.strip()
                if text:
                    if elements_stack:
                        current_element = elements_stack[-1]
                        if current_element.tag in self.text_related_elements:
                            if not current_element.text:
                                current_element.text = text
                            else:
                                current_element.text += ' ' + text
                    else:
                        continue

        if elements_stack:
            return elements_stack[0]
        return current_element

    
    def parse_tag(self, token: str) -> tuple[str, dict]:
        """Parses an opening tag and extracts the tag name and attributes."""
        tag_match = re.match(r"<(\w+)", token)
        tag_name = tag_match.group(1) if tag_match else None
        attributes = {}

        attr_matches = re.findall(r'(\w+)=["\']([^"\']+)["\']', token)
        for attr_name, attr_value in attr_matches:
            attributes[attr_name] = attr_value

        return tag_name, attributes


    def classify_element(self, tag_name: str, attributes: dict):
        """Classifies the element by tag name and returns the appropriate HTMLElement subclass."""

        if tag_name == "div":
            return HTMLDivElement(attributes=attributes)
        elif tag_name == "body":
            return HTMLBodyElement(attributes=attributes)
        elif tag_name == "head":
            return HTMLHeadElement(attributes=attributes)
        elif tag_name == "link":
            return HTMLLinkElement(attributes=attributes)
        else:
            # print("got: " + tag_name)
            return HTMLElement(tag=tag_name, attributes=attributes)

