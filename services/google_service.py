import requests

from services.html_service import HtmlService


class GoogleService:
    def __init__(self, html_service: HtmlService):
        self.html_service = html_service

    def search(self, query: str) -> list[str]:
        url = f'https://www.google.com/search?q={query}'
        response = requests.get(url)
        data = response.text
        self.html_service.feed(data)
        return self.html_service.results
