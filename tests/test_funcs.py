import os
import logging
import responses
from testfixtures import log_capture
from unittest.mock import patch
from helm_upgrade.app import check_chart_versions
from helm_upgrade.app import get_local_chart_versions
from helm_upgrade.app import get_remote_chart_versions
from helm_upgrade.app import pull_version_from_chart_file
from helm_upgrade.app import pull_version_from_github_pages
from helm_upgrade.app import pull_version_from_github_releases

HERE = os.getcwd()


def test_check_chart_versions_match():
    test_current_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }
    test_new_deps = test_current_deps.copy()

    result = check_chart_versions(test_current_deps, test_new_deps)

    assert len(result) == 0
    assert result == []


def test_check_chart_versions_no_match():
    test_current_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }
    test_new_deps = {
        "dog": 1,
        "cat": 5,
        "tree": 3,
    }

    result = check_chart_versions(test_current_deps, test_new_deps)

    assert len(check_chart_versions(test_current_deps, test_new_deps)) == 1
    assert result == ["cat"]


@log_capture()
def test_check_chart_versions_match_verbose(capture):
    logger = logging.getLogger()
    logger.info("All charts are up-to-date!")

    test_current_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }
    test_new_deps = test_current_deps.copy()

    result = check_chart_versions(
        test_current_deps, test_new_deps, verbose=True
    )  # noqa: E501

    assert len(result) == 0
    assert result == []
    capture.check_present()


@log_capture()
def test_check_chart_versions_no_match_verbose(capture):
    logger = logging.getLogger()
    logger.info("New versions are available.\n\t\tcat: 2 --> 5")

    test_current_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }
    test_new_deps = {
        "dog": 1,
        "cat": 5,
        "tree": 3,
    }

    result = check_chart_versions(
        test_current_deps, test_new_deps, verbose=True
    )  # noqa: E501

    assert len(check_chart_versions(test_current_deps, test_new_deps)) == 1
    assert result == ["cat"]
    capture.check_present()


def test_get_local_chart_versions():
    chart_name = os.path.join("tests", "test-chart")
    test_deps = {
        "binderhub": "0.2.0-n079.h351d336",
        "nginx-ingress": "1.29.5",
        "cert-manager": "v0.10.0",
    }

    assert get_local_chart_versions(chart_name) == test_deps


def test_get_local_chart_versions_broken():
    chart_name = os.path.join("tests", "test-chart")
    test_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }

    assert get_local_chart_versions(chart_name) != test_deps


@log_capture()
def test_get_local_chart_versions_verbose(capture):
    chart_name = os.path.join("tests", "test-chart")
    filepath = os.path.join(HERE, chart_name, "requirements.yaml")

    logger = logging.getLogger()
    logger.info("Reading local chart dependencies from: %s" % filepath)

    test_deps = {
        "binderhub": "0.2.0-n079.h351d336",
        "nginx-ingress": "1.29.5",
        "cert-manager": "v0.10.0",
    }

    result = get_local_chart_versions(chart_name, verbose=True)

    assert result == test_deps
    capture.check_present()


@log_capture()
def test_get_local_chart_versions_broken_verbose(capture):
    chart_name = os.path.join("tests", "test-chart")
    filepath = os.path.join(HERE, chart_name, "requirements.yaml")

    logger = logging.getLogger()
    logger.info("Reading local chart dependencies from: %s" % filepath)

    test_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }

    result = get_local_chart_versions(chart_name, verbose=True)

    assert result != test_deps
    capture.check_present()


@responses.activate
def test_pull_version_from_chart_file():
    test_dict = {}
    test_dep = "dependency"
    test_url = "http://jsonplaceholder.typicode.com/Chart.yaml"

    responses.add(
        responses.GET, test_url, json={"version": "1.2.3"}, status=200,
    )

    test_dict = pull_version_from_chart_file(test_dict, test_dep, test_url)

    assert len(test_dict) == 1
    assert list(test_dict.items()) == [(test_dep, "1.2.3")]

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert responses.calls[0].response.text == '{"version": "1.2.3"}'


@responses.activate
def test_pull_version_from_github_pages():
    test_dict = {}
    test_dep = "dependency"
    test_url = "http://jsonplaceholder.typicode.com/gh-pages/index.yaml"

    responses.add(
        responses.GET,
        test_url,
        json={
            "entries": {
                "dependency": [
                    {
                        "created": "2020-07-26T15:33:00.0000000Z",
                        "version": "1.2.3",
                    },  # noqa: E501
                    {
                        "created": "2020-07-25T15:33:00.0000000Z",
                        "version": "1.2.2",
                    },  # noqa: E501
                ]
            }
        },
        status=200,
    )

    test_dict = pull_version_from_github_pages(test_dict, test_dep, test_url)

    assert len(test_dict) == 1
    assert list(test_dict.items()) == [(test_dep, "1.2.3")]

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert (
        responses.calls[0].response.text
        == '{"entries": {"dependency": [{"created": "2020-07-26T15:33:00.0000000Z", "version": "1.2.3"}, {"created": "2020-07-25T15:33:00.0000000Z", "version": "1.2.2"}]}}'  # noqa: E501
    )


@responses.activate
def test_pull_version_from_github_releases():
    test_dict = {}
    test_dep = "dependency"
    test_url = "http://jsonplaceholder.typicode.com/releases/latest/"

    desired_version = "v1.2.3"
    responses.add(
        responses.GET,
        test_url,
        body=f'<html lang="en"><a href="/user/repo/tree/{desired_version}" title="{desired_version}"><span>{desired_version}</span></a></html>',  # noqa: E501
        status=200,
    )

    test_dict = pull_version_from_github_releases(
        test_dict, test_dep, test_url
    )  # noqa: E501

    assert len(test_dict) == 1
    assert list(test_dict.items()) == [(test_dep, "v1.2.3")]

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert (
        responses.calls[0].response.text
        == f'<html lang="en"><a href="/user/repo/tree/{desired_version}" title="{desired_version}"><span>{desired_version}</span></a></html>'  # noqa: E501
    )


@patch(
    "helm_upgrade.app.pull_version_from_chart_file",
    return_value={"nginx-ingress": "1.2.3"},
)
def test_get_remote_chart_versions_from_chart(mocked_func):
    test_deps = {
        "nginx-ingress": "https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml"  # noqa: E501
    }
    test_result = get_remote_chart_versions(test_deps)

    assert test_result == {"nginx-ingress": "1.2.3"}
    assert mocked_func.call_count == 1


@patch(
    "helm_upgrade.app.pull_version_from_chart_file",
    return_value={"nginx-ingress": "1.2.3"},
)
@log_capture
def test_get_remote_chart_versions_from_chart_verbose(mocked_func, capture):
    test_deps = {
        "nginx-ingress": "https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml"  # noqa: E501
    }

    logger = logging.getLogger()
    logger.info(
        """Retrieving the most recent version of
                chart: nginx-ingress
                repository: https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml"""  # noqa: E501
    )

    test_result = get_remote_chart_versions(test_deps, verbose=True)

    assert test_result == {"nginx-ingress": "1.2.3"}
    assert mocked_func.call_count == 1
    capture.check_present()
