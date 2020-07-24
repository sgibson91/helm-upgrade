"""Update Helm Chart dependencies."""
import os
import yaml
import logging
import requests

import numpy as np

from bs4 import BeautifulSoup
from itertools import compress

HERE = os.getcwd()
ABSOLUTE_HERE = os.path.dirname(os.getcwd())


def logging_config():
    """Enable logging configuration."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_request(url, content=False, text=False):
    """Send a HTTP GET request to a target URL. Return payload as JSON or html
    content.

    Args:
        url (str): The URL to send the request to
        content (bool, optional): Return the payload as HTML content.
                                  Defaults to False.
        text (bool, optional): Return the payload as text content.
                               Defaults to False.
    """
    if content and text:
        raise Exception("Cannot return both HTML and text content.")

    resp = requests.get(url)

    if not resp:
        raise Exception(f"Response not returned by URL: {url}")

    if content:
        return resp.content
    elif text:
        return resp.text
    else:
        return resp


def update_requirements_file(
    chart_name: str,
    charts: list,
    remote_dependencies: dict,
    verbose: bool = False,  # noqa: E501
):
    file_path = os.path.join(HERE, chart_name, "requirements.yaml")

    with open(file_path, "r") as stream:
        chart_yaml = yaml.safe_load(stream)

    for chart in charts:
        if verbose:
            logging.info("Updating version for: %s" % chart)

        for dependency in chart_yaml["dependencies"]:
            if dependency["name"] == chart:
                dependency["version"] = remote_dependencies[chart]

    with open(file_path, "w") as stream:
        yaml.safe_dump(chart_yaml, stream)

    if verbose:
        logging.info("Updated requirements in: %s" % file_path)


def check_chart_versions(
    chart_name: str,
    dependencies: dict,
    local_dependencies: dict,
    remote_dependencies: dict,
    dry_run: bool = False,
    verbose: bool = False,
) -> bool:
    charts = list(dependencies.keys())
    condition = [
        (local_dependencies[chart] != remote_dependencies[chart])
        for chart in charts  # noqa: E501
    ]

    if np.any(condition):
        if verbose:
            logging.info(
                "New versions are available.\n\t\t"
                + "\n\t\t".join(
                    [
                        (
                            f"{chart}: {local_dependencies[chart]} --> {remote_dependencies[chart]}"  # noqa: E501
                        )
                        for chart in charts
                    ]
                )
            )
        return list(compress(charts, condition))

    else:
        if verbose:
            logging.info("All charts are up-to-date!")

        return []


def pull_version_from_chart_file(
    remote_dependencies: dict, name: str, url: str
) -> dict:
    chart_reqs = yaml.safe_load(get_request(url, text=True))
    remote_dependencies[name] = chart_reqs["version"]

    return remote_dependencies


def pull_version_from_github_pages(
    remote_dependencies: dict, name: str, url: str
) -> dict:
    chart_reqs = yaml.safe_load(get_request(url, text=True))
    updates_sorted = sorted(
        chart_reqs["entries"][name], key=lambda k: k["created"]
    )  # noqa: E501
    remote_dependencies[name] = updates_sorted[-1]["version"]

    return remote_dependencies


def pull_version_from_github_releases(
    remote_dependencies: dict, name: str, url: str
) -> dict:
    res = get_request(url, content=True)
    soup = BeautifulSoup(res, "html.parser")

    links = soup.find_all("a", attrs={"title": True})

    for link in links:
        if (
            (link.span is not None)
            and ("v" in link.span.text)
            and ("." in link.span.text)
        ):

            remote_dependencies[name] = link.span.text

    return remote_dependencies


def get_remote_chart_versions(
    dependencies: dict, verbose: bool = False
) -> dict:  # noqa: E501
    remote_dependencies = {}

    for dependency in dependencies.keys():
        if verbose:
            logging.info(
                """Retrieving the most recent version of
                        chart: %s
                        repository: %s"""
                % (dependency, dependencies[dependency])
            )

        if dependencies[dependency].endswith("Chart.yaml"):
            remote_dependencies = pull_version_from_chart_file(
                remote_dependencies,
                name=dependency,
                url=dependencies[dependency],  # noqa: E501
            )

        elif "/gh-pages/" in dependencies[dependency]:
            remote_dependencies = pull_version_from_github_pages(
                remote_dependencies,
                name=dependency,
                url=dependencies[dependency],  # noqa: E501
            )

        elif dependencies[dependency].endswith("/releases/latest"):
            remote_dependencies = pull_version_from_github_releases(
                remote_dependencies,
                name=dependency,
                url=dependencies[dependency],  # noqa: E501
            )

        else:
            raise Exception(
                f"Chart type not recognised: {dependencies[dependency]}"  # noqa: E501
            )

    return remote_dependencies


def get_local_chart_versions(chart_name: str, verbose: bool = False) -> dict:
    local_dependencies = {}

    filepath = os.path.join(HERE, chart_name, "requirements.yaml")

    if verbose:
        logging.info(
            "Reading local chart dependencies from: %s" % filepath
        )  # noqa: E501

    with open(filepath, "r") as stream:
        chart_deps = yaml.safe_load(stream)

    for dependency in chart_deps["dependencies"]:
        local_dependencies[dependency["name"]] = dependency["version"]

    return local_dependencies


def helm_upgrade(
    chart_name: str,
    dependencies: dict,
    dry_run: bool = False,
    verbose: bool = False,  # noqa: E501
):
    # Turn on logging
    if verbose:
        logging_config()

    if dry_run and verbose:
        logging.info("THIS IS A DRY-RUN. NO FILES WILL BE CHANGED.")

    # Get local dependencies
    local_deps = get_local_chart_versions(chart_name, verbose=verbose)
    # Get remote dependencies
    remote_deps = get_remote_chart_versions(dependencies, verbose=verbose)
    # Check the chart versions
    charts_to_update = check_chart_versions(
        chart_name,
        dependencies,
        local_deps,
        remote_deps,
        dry_run=dry_run,
        verbose=verbose,
    )

    if (len(charts_to_update) > 0) and (not dry_run):
        update_requirements_file(
            chart_name, charts_to_update, remote_deps, verbose=verbose
        )
