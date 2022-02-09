"""Update Helm Chart dependencies."""
import logging
import os
from itertools import compress

import numpy as np
import requests
import yaml
from bs4 import BeautifulSoup

HERE = os.getcwd()


def logging_config():
    """Enable logging configuration."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def update_requirements_file(
    chart_name: str,
    deps_to_update: list,
    deps: dict,
    verbose: bool = False,
):
    """Update the Helm Chart requirements.yaml file with new dependency versions

    Args:
        chart_name (str): The name of the helm chart
        deps_to_update (list): The dependencies to be updated
        deps (dict): The dependencies and their versions
        verbose (bool, optional): Produce verbose output. Defaults to False.
    """
    file_path = os.path.join(HERE, chart_name, "requirements.yaml")

    with open(file_path, "r") as stream:
        chart_yaml = yaml.safe_load(stream)

    for dep in deps_to_update:
        if verbose:
            logging.info("Updating version for: %s" % dep)

        for dependency in chart_yaml["dependencies"]:
            if dependency["name"] == dep:
                dependency["version"] = deps[dep]

    with open(file_path, "w") as stream:
        yaml.safe_dump(chart_yaml, stream)

    if verbose:
        logging.info("Updated requirements in: %s" % file_path)


def check_chart_versions(
    current_deps: dict,
    new_deps: dict,
    verbose: bool = False,
) -> list:
    """Check whether the versions of the charts in the current dependencies are
    up-to-date with the remote ones.

    Args:
        current_deps (dict): The versions the helm chart is currently running
        new_deps (dict): Newer versions of the dependencies
        verbose (bool, optional): Produce verbose output. Defaults to False.

    Returns:
        list: A list of the dependencies that need updating
    """
    charts = list(current_deps.keys())
    condition = [(current_deps[chart] != new_deps[chart]) for chart in charts]

    if np.any(condition):
        if verbose:
            logging.info(
                "New versions are available.\n\t\t"
                + "\n\t\t".join(
                    [
                        (
                            f"{chart}: {current_deps[chart]} --> {new_deps[chart]}"  # noqa: E501
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
    output_dict: dict, dependency: str, url: str
) -> dict:  # noqa: E501
    """Pull recent, up-to-date version from remote host stored in a Chart.yml
    file.

    Args:
        output_dict (dict): The dictionary to store versions in
        dependency (str): The dependency to get a new version for
        url (str): The URL of the remotely hosted versions
    """
    chart_reqs = yaml.safe_load(get_request(url))
    output_dict[dependency] = chart_reqs["version"]

    return output_dict


def pull_version_from_github_pages(
    output_dict: dict, dependency: str, url: str
) -> dict:
    """Pull recent, up-to-date version from remote host listed on a GitHub Pages
    site.

    Args:
        output_dict (dict): The dictionary to store versions in
        dependency (str): The dependency to get a version for
        url (str): The URL of the remotely hosted versions
    """
    chart_reqs = yaml.safe_load(get_request(url))
    updates_sorted = sorted(
        chart_reqs["entries"][dependency], key=lambda k: k["created"]
    )
    output_dict[dependency] = updates_sorted[-1]["version"]

    return output_dict


def pull_version_from_github_releases(
    output_dict: dict, dependency: str, url: str
) -> dict:
    """Pull recent, up-to-date version from remote host listed on a GitHub
    Releases site.

    Args:
        output_dict (dict): The dictionary to store versions in
        dependency (str): The dependency to get a version for
        url (str): The URL of the remotely hosted versions
    """
    res = get_request(url)
    soup = BeautifulSoup(res, "html.parser")

    links = soup.find_all("a", attrs={"title": True})

    for link in links:
        if (
            (link.span is not None)
            and ("v" in link.span.text)
            and ("." in link.span.text)
        ):

            output_dict[dependency] = link.span.text

    return output_dict


def get_remote_chart_versions(deps: dict, verbose: bool = False) -> dict:
    """Get dependency versions from the remote hosts

    Args:
        deps (dict): The dependencies to check and their host URLs
        dependency (str): The dependency to get a version for
        verbose (bool, optional): Produce verbose output. Defaults to False.

    Returns:
        dict: The dependencies and the most recent versions from the remote
              hosts
    """
    remote_dependencies = {}

    for dep in deps.keys():
        if verbose:
            logging.info(
                """Retrieving the most recent version of
                        chart: %s
                        repository: %s"""
                % (dep, deps[dep])
            )

        if deps[dep].endswith("Chart.yaml"):
            remote_dependencies = pull_version_from_chart_file(
                remote_dependencies,
                dep,
                deps[dep],
            )

        elif "/gh-pages/" in deps[dep]:
            remote_dependencies = pull_version_from_github_pages(
                remote_dependencies,
                dep,
                deps[dep],
            )

        elif deps[dep].endswith("/releases/latest"):
            remote_dependencies = pull_version_from_github_releases(
                remote_dependencies,
                dep,
                deps[dep],
            )

        else:
            raise Exception(f"Chart type not recognised: {deps[dep]}")

    return remote_dependencies


def get_local_chart_versions(chart_name: str, verbose: bool = False) -> dict:
    """The dependency versions currently being installed by the helm chart

    Args:
        chart_name (str): The name of the local helm chart
        verbose (bool, optional): Produce verbose output. Defaults to False.
    """
    local_dependencies = {}

    filepath = os.path.join(HERE, chart_name, "requirements.yaml")

    if verbose:
        logging.info("Reading local chart dependencies from: %s" % filepath)

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
    """Upgrade a local helm chart's requirements.yaml to have up-to-date
    versions of its dependencies.

    Args:
        chart_name (str): The name of the helm chart
        dependencies (dict): A list of dependencies to check and host URLs
        dry_run (bool, optional): Don't change any files. Defaults to False.
        verbose (bool, optional): Produce verbose output. Defaults to False.
    """
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
        local_deps, remote_deps, verbose=verbose
    )  # noqa: E501

    if (len(charts_to_update) > 0) and (not dry_run):
        update_requirements_file(
            chart_name, charts_to_update, remote_deps, verbose=verbose
        )
