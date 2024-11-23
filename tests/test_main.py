import subprocess
import sys

import io
import pytest
from factory import Factory, Faker

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

class ArticleFactory(Factory):
    class Meta:
        model = Article

    title = Faker('sentence')
    extract = Faker('paragraph')

def parametrized_fixture(*params):
    return pytest.fixture(params=params)(lambda request: params)

article = parametrized_fixture(*ArticleFactory.build_batch(10))


@pytest.fixture(params=articles)
def article(request):
    return request.param

# articlesの各記事に対してテストを行う
def test_final_newline(article, file):
    article = Article(title="Lorem Ipsum", extract="Lorem ipsum dolor sit amet.")
    file = io.StringIO()
    show(article, file)
    assert file.getvalue().endswith("\n")



@pytest.fixture(name='serve')
def serve(httpserver):

    def f(article):
        json = {'title': article.title, 'extract': article.extract}
        httpserver.expect_request('/').respond_with_json(json)
        return httpserver.url_for('/')

    return f


def test_fetch(article, serve):

    assert article == fetch(serve(article))

