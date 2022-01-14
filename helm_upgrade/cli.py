import argparse
import json
import os
import sys

from .app import helm_upgrade

HERE = os.path.abspath(os.path.dirname(__file__))


def parse_args(args):
    """Parse arguments from the command line"""
    DESCRIPTION = "Update the dependencies of a local Helm Chart in a project repository."  # noqa: E501
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    subparsers = parser.add_subparsers()

    version_parser = subparsers.add_parser(  # noqa: F841
        "version", help="Print the version and exit"
    )  # noqa: E501

    run_parser = subparsers.add_parser(
        "run", help="Update the dependencies of a helm chart"
    )

    run_parser.add_argument(
        "chart", type=str, help="Name of the local Helm Chart to be updated."
    )

    run_parser.add_argument(
        "dependencies",
        type=json.loads,
        help="""A dictionary of Helm Chart dependencies and their host repo URLs.
        E.g. '{"nginx-ingress":
        "https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml"}'
        """,
    )

    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run of the update. Don't write the changes to a file.",  # noqa: E501
    )

    run_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Option to turn on logging.",  # noqa: E501
    )

    return parser.parse_args()


def main():
    """Main function"""
    args = parse_args(sys.argv[1:])

    if not vars(args):
        about = {}

        with open(os.path.join(HERE, "__version__.py")) as f:
            exec(f.read(), about)

        print(about["__version__"])

    else:
        helm_upgrade(
            args.chart,
            args.dependencies,
            dry_run=args.dry_run,
            verbose=args.verbose,  # noqa: E501
        )


if __name__ == "__main__":
    main()
