import re
from typing import List, Optional

class HTMLTokenizer:
    def __init__(self, html: str):
        self.html = html
        self.position = 0
        self.tokens = self.tokenize()

    def tokenize(self) -> List[str]:
        """Tokenizes the HTML into a list of tags and text."""
        # Matches tags and text between tags
        tag_regex = r"(<[^>]+>|[^<]+)"
        return re.findall(tag_regex, self.html)

    def next_token(self) -> Optional[str]:
        """Returns the next token or None if end of tokens."""
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token.strip() if token.strip() else self.next_token()
        return None
