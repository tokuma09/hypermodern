from hyper_tokuma.random_wikipedia import build_user_agent


def test_build_user_agent():
    assert 'hyper_tokuma' in build_user_agent()
