import subprocess
import sys

import io
import pytest
from contextlib import contextmanager

import http.server
import json
import threading

from hyper_tokuma.random_wikipedia import Article, show, fetch
def test_output():

    args = [sys.executable, '-m', "hyper_tokuma"]
    result = subprocess.run(args,capture_output=True, check=True)

    assert result.stdout


@pytest.fixture(name='file')
def file():
    return io.StringIO()


articles = [
    Article(),
    Article('test'),
    Article(title="Lorem Ipsum", extract="Lorem ipsum dolor sit amet."),
    Article("Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Nulla mattis volutpat sapien, at dapibus ipsum accumsan eu."),
]

@pytest.fixture(params=articles)
def article(request):
    return request.param

# articlesの各記事に対してテストを行う
def test_final_newline(article, file):
    article = Article(title="Lorem Ipsum", extract="Lorem ipsum dolor sit amet.")
    file = io.StringIO()
    show(article, file)
    assert file.getvalue().endswith("\n")




@pytest.fixture(scope='session')
def http_server():
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            article = self.server.article
            data = {"title": article.title, "extract": article.extract}
            body = json.dumps(data).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    with http.server.HTTPServer(('localhost', 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield server
        server.shutdown()
        thread.join()


@pytest.fixture(name='serve')
def serve(http_server):

    def f(article):
        http_server.article = article
        return f"http://localhost:{http_server.server_port}"

    return f


def test_fetch(article, serve):

    assert article == fetch(serve(article))

