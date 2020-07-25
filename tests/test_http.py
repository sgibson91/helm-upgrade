from unittest.mock import Mock, patch
from helm_upgrade.app import get_request


@patch("helm_upgrade.app.requests.get")
def test_get_request(mock_get):
    test_url = "http://jsonplaceholder.typicode.com"
    mock_get.return_value = Mock(ok=True, text='{"test-1": 1, "test-2": 2}')
    resp = get_request(test_url)

    assert resp.ok
    assert resp.text == '{"test-1": 1, "test-2": 2}'


@patch("helm_upgrade.app.requests.get")
def test_get_request_broken(mock_get):
    test_url = "http://josnplaceholder.typicode.com"
    mock_get.return_value = Mock(ok=False, text=None)
    resp = get_request(test_url)

    assert not resp.ok
    assert resp.text is None
