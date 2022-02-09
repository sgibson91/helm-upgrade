import os
from subprocess import check_call
from unittest.mock import patch

import responses
import yaml

from helm_upgrade.app import (
    check_chart_versions,
    get_local_chart_versions,
    get_remote_chart_versions,
    pull_version_from_chart_file,
    pull_version_from_github_pages,
    pull_version_from_github_releases,
    update_requirements_file,
)

HERE = os.getcwd()


# Helper function: Not a test!
def checkout_file(filepath):
    check_call(["git", "checkout", "--", filepath])


# === Tests === #


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


def test_get_local_chart_versions():
    chart_path = os.path.join("tests", "test-chart", "requirements.yaml")
    test_deps = {
        "binderhub": "0.2.0-n079.h351d336",
        "nginx-ingress": "1.29.5",
        "cert-manager": "v0.10.0",
    }

    assert get_local_chart_versions(chart_path) == test_deps


def test_get_local_chart_versions_broken():
    chart_path = os.path.join("tests", "test-chart", "requirements.yaml")
    test_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }

    assert get_local_chart_versions(chart_path) != test_deps


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
                    },
                    {
                        "created": "2020-07-25T15:33:00.0000000Z",
                        "version": "1.2.2",
                    },
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
        == '{"entries": {"dependency": [{"created": "2020-07-26T15:33:00.0000000Z", "version": "1.2.3"}, {"created": "2020-07-25T15:33:00.0000000Z", "version": "1.2.2"}]}}'
    )


@responses.activate
def test_pull_version_from_github_releases():
    test_dict = {}
    test_dep = "dependency"
    test_url = "http://jsonplaceholder.typicode.com/releases/latest/"

    responses.add(
        responses.GET,
        test_url,
        body='<html lang="en"><title>Release v1.7.1 · cert-manager/cert-manager · GitHub</title</html>',
        status=200,
    )

    test_dict = pull_version_from_github_releases(test_dict, test_dep, test_url)

    assert len(test_dict) == 1
    assert list(test_dict.items()) == [(test_dep, "v1.7.1")]

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_url
    assert (
        responses.calls[0].response.text
        == '<html lang="en"><title>Release v1.7.1 · cert-manager/cert-manager · GitHub</title</html>'
    )


@patch(
    "helm_upgrade.app.pull_version_from_chart_file",
    return_value={"nginx-ingress": "1.2.3"},
)
def test_get_remote_chart_versions_from_chart(mocked_func):
    test_deps = {
        "nginx-ingress": "https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml"
    }
    test_result = get_remote_chart_versions(test_deps)

    assert test_result == {"nginx-ingress": "1.2.3"}
    assert mocked_func.call_count == 1


@patch(
    "helm_upgrade.app.pull_version_from_github_pages",
    return_value={"binderhub": "1.2.3"},
)
def test_get_remote_chart_versions_from_github_pages(mocked_func):
    test_deps = {
        "binderhub": "https://raw.githubusercontent.com/jupyterhub/helm-chart/gh-pages/index.yaml"
    }
    test_result = get_remote_chart_versions(test_deps)

    assert test_result == {"binderhub": "1.2.3"}
    assert mocked_func.call_count == 1


@patch(
    "helm_upgrade.app.pull_version_from_github_releases",
    return_value={"cert-manager": "v1.2.3"},
)
def test_get_remote_chart_versions_from_github_releases(mocked_func):
    test_deps = {
        "cert-manager": "https://github.com/jetstack/cert-manager/releases/latest"
    }
    test_result = get_remote_chart_versions(test_deps)

    assert test_result == {"cert-manager": "v1.2.3"}
    assert mocked_func.call_count == 1


def test_update_requirements_file():
    chart_path = os.path.join("tests", "test-chart", "requirements.yaml")
    deps_to_update = ["binderhub", "cert-manager", "nginx-ingress"]
    deps_dict = {
        "binderhub": "1.2.3",
        "cert-manager": "v1.2.3",
        "nginx-ingress": "1.2.3",
    }

    checkout_file(chart_path)

    # Read in current deps
    with open(chart_path, "r") as stream:
        deps_before = yaml.safe_load(stream)

    update_requirements_file(chart_path, deps_to_update, deps_dict)

    # Read in edited deps
    with open(chart_path, "r") as stream:
        deps_after = yaml.safe_load(stream)

    assert deps_before != deps_after
