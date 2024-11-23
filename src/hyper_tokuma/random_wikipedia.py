import textwrap
import httpx
from rich.console import Console

from importlib.metadata import metadata

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
USER_AGENT = "{NAME}/{VERSION} (Contract {Author-email})"

def build_user_agent():
    fields = metadata("hyper-tokuma")
    return USER_AGENT.format_map(fields)

def main():
    headers = {"User-Agent": build_user_agent()}

    with httpx.Client(headers=headers, http2=True, follow_redirects=True) as client:
        response = client.get(API_URL)
        response.raise_for_status()
        data = response.json()

    console = Console(width=72, highlight=False)
    console.print(data['title'], style="bold", end="\n\n")
    console.print(data['extract'])

