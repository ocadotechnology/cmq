import os
import pytest
from cmq.base import Session
from mock_resources import (
    MockSession,
)


def test_resource_interface_chain():
    parent = MockSession(None)
    child = MockSession(parent)
    assert parent._child == child
    assert child._parent == parent


def test_resource_interface_root():
    parent = MockSession(None)
    child = MockSession(parent)
    assert child.root() == parent


def test_paged_resource():
    resource = MockSession(None)
    results = resource.paginate({})
    assert results == [1,2,3,4,5,6]


def test_session_base_get_sessions_signature():
    session = Session(None)
    with pytest.raises(NotImplementedError):
        session.get_sessions()


def test_session_mock_get_sessions():
    session = MockSession(None)
    sessions = session.get_sessions()
    assert len(sessions) == 3
    assert sessions[0]["id"] == "111111111111"


def test_pep561_py_typed_present():
    import cmq
    pkg_dir = os.path.dirname(cmq.__file__)
    py_typed_path = os.path.join(pkg_dir, "py.typed")
    assert os.path.isfile(py_typed_path)

