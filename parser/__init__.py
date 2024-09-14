import re
from tokenizer import HTMLTokenizer
from htypes import HTMLElement, HTMLHeadElement, HTMLBodyElement, HTMLDivElement, HTMLLinkElement, HTMLPlainText

class HTMLParser:
    def __init__(self, html: str):
        self.tokenizer = HTMLTokenizer(html)
        self.root = None
        # Define valid text-related elements
        self.text_related_elements = {"title", "p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "a", "div", "body"}

    def parse(self) -> HTMLElement:
        """Starts parsing and returns the root element of the parsed HTML tree."""
        elements_stack = []
        current_element = None

        while True:
            token = self.tokenizer.next_token()
            if token is None:
                break

            if token.startswith("</"):  # Closing tag
                if elements_stack:
                    finished_element = elements_stack.pop()
                    if elements_stack:
                        elements_stack[-1].children.append(finished_element)
                    else:
                        current_element = finished_element

            elif token.startswith("<"):  # Opening tag
                tag_name, attributes = self.parse_tag(token)
                element = self.classify_element(tag_name, attributes)

                if tag_name in ["br", "img", "input", "meta", "link", "hr"]:  # Self-closing elements
                    if elements_stack:
                        elements_stack[-1].children.append(element)
                else:
                    elements_stack.append(element)

            else:  # This is a text node (between opening and closing tags)
                text = token.strip()
                if text:
                    if elements_stack:
                        current_element = elements_stack[-1]
                        if current_element.tag in self.text_related_elements:
                            # Instead of adding text as a child, set it in the text attribute
                            if not current_element.text:
                                current_element.text = text
                            else:
                                # If there's already text, append it (handles cases with multiple text nodes)
                                current_element.text += ' ' + text
                    else:
                        # Ignore free-floating text outside elements
                        continue

        if elements_stack:
            return elements_stack[0]
        return current_element

    
    def parse_tag(self, token: str) -> tuple[str, dict]:
        """Parses an opening tag and extracts the tag name and attributes."""
        tag_match = re.match(r"<(\w+)", token)
        tag_name = tag_match.group(1) if tag_match else None
        attributes = {}

        # Regular expression to match attributes in the form of key="value"
        attr_matches = re.findall(r'(\w+)=["\']([^"\']+)["\']', token)
        for attr_name, attr_value in attr_matches:
            attributes[attr_name] = attr_value

        return tag_name, attributes


    def classify_element(self, tag_name: str, attributes: dict) -> HTMLElement:
        """Classifies the element by tag name and returns the appropriate HTMLElement subclass."""
        # Ensure attributes are parsed only from valid tokens
        if tag_name == "div":
            return HTMLDivElement(attributes=attributes)
        elif tag_name == "body":
            return HTMLBodyElement(attributes=attributes)
        elif tag_name == "head":
            return HTMLHeadElement(attributes=attributes)
        elif tag_name == "link":
            return HTMLLinkElement(attributes=attributes)
        else:
            return HTMLElement(tag=tag_name, attributes=attributes)

