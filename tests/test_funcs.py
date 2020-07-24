from helm_upgrade.app import check_chart_versions


def test_check_chart_versions_match():
    test_current_deps = {
        "dog": 1,
        "cat": 2,
        "tree": 3,
    }
    test_new_deps = test_current_deps.copy()

    assert check_chart_versions(test_current_deps, test_new_deps) == []
