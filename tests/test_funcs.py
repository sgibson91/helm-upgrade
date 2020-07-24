import os
import logging
from testfixtures import log_capture
from helm_upgrade.app import check_chart_versions, get_local_chart_versions


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

    assert len(check_chart_versions(test_current_deps, test_new_deps)) == 1
    assert check_chart_versions(test_current_deps, test_new_deps) == ["cat"]


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
