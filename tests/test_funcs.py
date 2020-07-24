from helm_upgrade.app import check_chart_versions


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
