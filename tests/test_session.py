from mock_resources import MockSession


def test_session_list():
    session = MockSession(None)
    accounts = session.list()

    assert isinstance(accounts, list)
    assert len(accounts) == 3


def test_session_dict():
    session = MockSession(None)
    accounts = session.dict()

    assert isinstance(accounts, dict)
    assert len(accounts) == 3