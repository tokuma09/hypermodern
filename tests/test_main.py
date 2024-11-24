import subprocess
import sys

import io
import pytest
from factory import Factory, Faker

from hyper_tokuma.random_wikipedia import Article, show, fetch



@pytest.fixture(name='file')
def file():
    return io.StringIO()


@pytest.fixture(name='serve')
def serve(httpserver):

    def f(article):
        json = {'title': article.title, 'extract': article.extract}
        httpserver.expect_request('/').respond_with_json(json)
        return httpserver.url_for('/')

    return f

class ArticleFactory(Factory):
    class Meta:
        model = Article

    title = Faker('sentence')
    extract = Faker('paragraph')


def parametrized_fixture(*params):
    return pytest.fixture(params=params)(lambda request: request.param)


article = parametrized_fixture(Article("test"), *ArticleFactory.build_batch(10))


def test_trailing_blank_line(article, file):

    show(article, file)
    assert not file.getvalue().endswith("\n\n")

# articlesの各記事に対してテストを行う
def test_final_newline(article, file):

    file = io.StringIO()
    show(article, file)
    assert file.getvalue().endswith("\n")


def test_fetch(article, serve):

    assert article == fetch(serve(article))

def test_output():

    args = [sys.executable, '-m', "hyper_tokuma"]
    result = subprocess.run(args,capture_output=True, check=True)

    assert result.stdout
