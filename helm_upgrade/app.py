import os
import re
from itertools import compress

import numpy as np
import requests
from bs4 import BeautifulSoup
from ruamel.yaml import YAML

HERE = os.path.abspath(os.getcwd())
yaml = YAML(typ="safe", pure=True)


def get_request(url: str):
    """Send a HTTP GET request to a target URL. Return payload as JSON.

    Args:
        url (str): The URL to send the request to
    """
    resp = requests.get(url)

    if not resp:
        raise Exception(f"Response not returned by URL: {url}")

    return resp.text


def update_requirements_file(
    chart_path: str,
    deps_to_update: list,
    deps: dict,
):
    """Update the local Helm Chart with new dependency versions

    Args:
        chart_path (str): Path to the file containing the dependencies of the
            local helm chart
        deps_to_update (list): The dependencies to be updated
        deps (dict): The dependencies and their versions
    """
    file_path = os.path.join(HERE, chart_path)

    with open(file_path) as stream:
        chart_yaml = yaml.load(stream)

    for dep in deps_to_update:
        for dependency in chart_yaml["dependencies"]:
            if dependency["name"] == dep:
                dependency["version"] = deps[dep]

    with open(file_path, "w") as stream:
        yaml.dump(chart_yaml, stream)


def check_chart_versions(
    current_deps: dict,
    new_deps: dict,
) -> list:
    """Check whether the versions of the charts in the current dependencies are
    up-to-date with the remote ones.

    Args:
        current_deps (dict): The versions the helm chart is currently running
        new_deps (dict): Newer versions of the dependencies

    Returns:
        list: A list of the dependencies that need updating
    """
    charts = list(current_deps.keys())
    condition = [(current_deps[chart] != new_deps[chart]) for chart in charts]

    if np.any(condition):
        return list(compress(charts, condition))
    else:
        return []


def pull_version_from_chart_file(output_dict: dict, dependency: str, url: str) -> dict:
    """Pull recent, up-to-date version from remote host stored in a Chart.yml
    file.

    Args:
        output_dict (dict): The dictionary to store versions in
        dependency (str): The dependency to get a new version for
        url (str): The URL of the remotely hosted versions
    """
    chart_reqs = yaml.load(get_request(url))
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
    chart_reqs = yaml.load(get_request(url))
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
    titles = soup.find_all("title")

    for title in titles:
        match = re.search(r"v[0-9]*\.[0-9]*\.[0-9]*", title.text)
        output_dict[dependency] = match.group(0)

    return output_dict


def get_remote_chart_versions(deps: dict) -> dict:
    """Get dependency versions from the remote hosts

    Args:
        deps (dict): The dependencies to check and their host URLs
        dependency (str): The dependency to get a version for

    Returns:
        dict: The dependencies and the most recent versions from the remote
              hosts
    """
    remote_dependencies = {}

    for dep in deps.keys():
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


def get_local_chart_versions(chart_path: str) -> dict:
    """The dependency versions currently being installed by the helm chart

    Args:
        chart_path (str): The path to the file containing the dependencies of
            the local helm chart
    """
    local_dependencies = {}

    filepath = os.path.join(HERE, chart_path)

    with open(filepath) as stream:
        chart_deps = yaml.load(stream)

    for dependency in chart_deps["dependencies"]:
        local_dependencies[dependency["name"]] = dependency["version"]

    return local_dependencies


def helm_upgrade(
    chart_path: str,
    dependencies: dict,
    dry_run: bool = False,
):
    """Upgrade a local helm chart to have up-to-date versions of its
    dependencies.

    Args:
        chart_path (str): The path to the file that contains the dependencies of
            the local helm chart to be updated
        dependencies (dict): A list of dependencies to check and host URLs
        dry_run (bool, optional): Don't change any files. Defaults to False.
    """
    # Get local dependencies
    local_deps = get_local_chart_versions(chart_path)
    # Get remote dependencies
    remote_deps = get_remote_chart_versions(dependencies)
    # Check the chart versions
    charts_to_update = check_chart_versions(local_deps, remote_deps)

    if (len(charts_to_update) > 0) and (not dry_run):
        update_requirements_file(chart_path, charts_to_update, remote_deps)
