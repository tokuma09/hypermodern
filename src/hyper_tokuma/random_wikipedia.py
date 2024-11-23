import textwrap
import httpx
from rich.console import Console

from dataclasses import dataclass
from importlib.metadata import metadata
import sys
API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
USER_AGENT = "{NAME}/{VERSION} (Contract {Author-email})"


@dataclass
class Article:
    title: str = ""
    extract: str = ""

def build_user_agent():
    fields = metadata("hyper-tokuma")
    return USER_AGENT.format_map(fields)

def fetch(url):
    headers = {"User-Agent": build_user_agent()}
    with httpx.Client(headers=headers, http2=True, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
    data = response.json()

    return Article(title=data['title'], extract=data['extract'])

def show(article, file):
    console = Console(file=file,width=72, highlight=False)
    console.print(article.title, style="bold", end="\n\n")
    console.print(textwrap.fill(article.extract, width=72))

def main():
    article = fetch(API_URL)
    show(article, sys.stdout)
