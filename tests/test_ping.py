from reddit_cli import ping


def test_ping():
    assert ping() == "pong"
