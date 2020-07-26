import pytest
import responses
from helm_upgrade.app import get_request


@responses.activate
def test_get_request():
    test_url = "http://jsonplaceholder.typicode.com/"

    responses.add(
        responses.GET,
        test_url,
        json={"key1": "value1"},
        status=200,
    )

    resp = get_request(test_url)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert responses.calls[0].response.text == '{"key1": "value1"}'

    assert resp == '{"key1": "value1"}'


@responses.activate
def test_get_request_broken():
    test_url = "http://jsonplaceholder.typicode.com/"

    with pytest.raises(Exception):
        get_request(test_url)
