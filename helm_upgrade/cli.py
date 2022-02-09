import argparse
import json
import os
import sys

from .app import helm_upgrade

HERE = os.path.abspath(os.path.dirname(__file__))


def parse_args(args):
    """Parse arguments from the command line"""
    DESCRIPTION = (
        "Update the dependencies of a local Helm Chart in a project repository."
    )
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        "chart_path",
        type=str,
        help="Path to the file containing the dependencies of the local Helm Chart to be updated.",
    )

    parser.add_argument(
        "dependencies",
        type=json.loads,
        help="""A dictionary of Helm Chart dependencies and their host repo URLs.
        E.g. '{"nginx-ingress":
        "https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml"}'
        """,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run of the update. Don't write the changes to a file.",
    )

    return parser.parse_args()


def main():
    """Main function"""
    args = parse_args(sys.argv[1:])

    helm_upgrade(
        args.chart_path,
        args.dependencies,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
