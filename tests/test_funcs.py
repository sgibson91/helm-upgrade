import os
import logging
import responses
from testfixtures import log_capture
from helm_upgrade.app import check_chart_versions, get_local_chart_versions
from helm_upgrade.app import pull_version_from_chart_file
from helm_upgrade.app import pull_version_from_github_pages

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
        responses.GET,
        test_url,
        json={"version": "1.2.3"},
        status=200,
    )

    test_dict = pull_version_from_chart_file(test_dict, test_dep, test_url)

    assert len(test_dict) == 1
    assert list(test_dict.items()) == [(test_dep, "1.2.3")]

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert responses.calls[0].response.text == '{"version": "1.2.3"}'
