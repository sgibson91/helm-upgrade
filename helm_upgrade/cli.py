import sys
import json
import argparse
from .app import helm_upgrade

DESCRIPTION = "Update the dependencies of a local Helm Chart in a project repository."  # noqa: E501
parser = argparse.ArgumentParser(description=DESCRIPTION)

parser.add_argument(
    "chart", type=str, help="Name of the local Helm Chart to be updated."
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

parser.add_argument(
    "-v", "--verbose", action="store_true", help="Option to turn on logging."
)


def main():
    """Main function"""
    args = parser.parse_args(sys.argv[1:])
    helm_upgrade(
        args.chart,
        args.dependencies,
        dry_run=args.dry_run,
        verbose=args.verbose,  # noqa: E501
    )


if __name__ == "__main__":
    main()
