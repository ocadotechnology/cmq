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
