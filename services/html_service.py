from html.parser import HTMLParser


class HtmlService(HTMLParser):
    def __init__(self):
        super().__init__()
        self._before_tag: str | None = None
        self._should_append: bool = False
        self.results: list[str] = []

    def feed(self, data: str) -> None:
        self.results = []
        super().feed(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and attr[1].startswith('/url?q='):
                    self._before_tag = tag
        elif tag == 'h3' and self._before_tag == 'a':
            self._before_tag = tag
        elif tag == 'div' and self._before_tag == 'h3':
            self._should_append = True
            self._before_tag = None
        else:
            self._before_tag = None

    def handle_data(self, data: str) -> None:
        if self._should_append:
            self.results.append(data)
            self._should_append = False
