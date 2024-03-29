import argparse
from unittest import mock

from helm_upgrade.cli import parse_args


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        chart="test-chart",
        dependencies={"test-dep-1": "v0.10.0", "test-dep-2": "0.19.5"},
    ),
)
def test_parser_basic(mock_args):
    parser = parse_args(
        [
            "test-chart",
            '{"test-dep-1": "v0.10.0", "test-dep-2": "0.19.5"}',
        ]
    )

    assert parser.chart == "test-chart"
    assert parser.dependencies == {
        "test-dep-1": "v0.10.0",
        "test-dep-2": "0.19.5",
    }


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        chart="test-chart",
        dependencies={"test-dep-1": "v0.10.0", "test-dep-2": "0.19.5"},
        dry_run=True,
    ),
)
def test_parser_dry_run(mock_args):
    parser = parse_args(
        [
            "test-chart",
            '{"test-dep-1": "v0.10.0", "test-dep-2": "0.19.5"}',
            "--dry-run",
        ]
    )

    assert parser.chart == "test-chart"
    assert parser.dependencies == {
        "test-dep-1": "v0.10.0",
        "test-dep-2": "0.19.5",
    }
    assert parser.dry_run is True
