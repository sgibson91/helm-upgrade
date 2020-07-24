import os
from helm_upgrade.app import check_chart_versions, get_local_chart_versions


def test_check_chart_versions_match():
    test_current_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }
    test_new_deps = test_current_deps.copy()

    assert len(check_chart_versions(test_current_deps, test_new_deps)) == 0
    assert check_chart_versions(test_current_deps, test_new_deps) == []


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


def test_get_local_chart_versions():
    chart_name = os.path.join("tests", "test-chart")
    test_deps = {
        "binderhub": "0.2.0-n079.h351d336",
        "nginx-ingress": "1.29.5",
        "cert-manager": "v0.10.0",
    }

    assert get_local_chart_versions(chart_name) == test_deps
