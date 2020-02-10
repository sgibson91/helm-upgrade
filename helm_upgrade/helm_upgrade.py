"""Update Helm Chart dependencies."""
import os
import yaml
import logging
import requests

import numpy as np

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


class HelmUpgrade:
    """HelmUpgrade class for interacting with the Helm Chart repos and making
    changes to a local Helm Chart requirements file

    Attributes:
        chart (str): The Helm Chart name
        dependencies (dict): A dictionary of helm chart dependencies and their
                             repos
        dry_run (Bool): Whether the changes should be pushed or not
        verbose (Bool): Whether to turn on logging or not
    """

    def __init__(self, argsDict):
        """The constructor for HelmUpgrade class

        Arguments:
            argsDict {dict} -- A dictionary of values parsed from argparse
        """
        for k, v in argsDict.items():
            setattr(self, k, v)

        # Turn on logging
        if self.verbose:
            logging_config()

        if self.dry_run and self.verbose:
            logging.info("THIS IS A DRY-RUN. NO FILES WILL BE CHANGED.")

    def check_chart_versions(self):
        """Check if Helm Chart versions match"""
        charts = list(self.dependencies.keys())
        condition = [
            (self.local_dependencies[chart] != self.remote_dependencies[chart])
            for chart in charts
        ]

        if np.any(condition):
            if self.verbose:
                logging.info(
                    "New versions are available.\n\t\t"
                    + "\n\t\t".join(
                        [
                            (
                                f"{chart}: {self.local_dependencies[chart]} --> {self.remote_dependencies[chart]}"
                            )
                            for chart in charts
                        ]
                    )
                )
                if self.dry_run:
                    logging.info("THIS IS A DRY-RUN. NO FILES WILL BE CHANGED.")
                else:
                    self.update_requirements_file(charts=list(compress(charts, condition)))
        else:
            if self.verbose:
                logging.info("All charts are up-to-date!")

    def get_chart_versions(self):
        """Automatically pull chart versions from local and remote hosts"""
        self.get_local_chart_versions()
        self.get_remote_chart_versions()

    def get_local_chart_versions(self):
        """Get the versions of the chart dependencies the local chart is
        currently pulling"""
        self.local_dependencies = {}

        filepath = os.path.join(HERE, self.chart, "requirements.yaml")

        if self.verbose:
            logging.info("Reading local chart dependencies from: %s" % filepath)

        with open(filepath, "r") as stream:
            chart_deps = yaml.safe_load(stream)

        for dependency in chart_deps["dependencies"]:
            self.local_dependencies[dependency["name"]] = dependency["version"]

    def get_remote_chart_versions(self):
        """Get the most recent version of the chart dependencies from the
        remote helm repository"""
        self.remote_dependencies = {}

        for dependency in self.dependencies.keys():
            if self.verbose:
                logging.info(
                    """Retrieving the most recent version of
                           chart: %s
                           repository: %s"""
                    % (dependency, self.dependencies[dependency],)
                )

            if self.dependencies[dependency].endswith("Chart.yaml"):
                self.pull_version_from_chart_file(
                    name=dependency, url=self.dependencies[dependency],
                )
            elif "/gh-pages/" in self.dependencies[dependency]:
                self.pull_version_from_github_pages(
                    name=dependency, url=self.dependencies[dependency],
                )

    def pull_version_from_chart_file(self, name, url):
        """Pull the version of a Helm Chart from it's Chart.yaml file

        Arguments:
            name {string} -- The name of the Helm Chart
            url {string} -- The URL of the Helm Chart's Chart.yaml file
        """
        chart_reqs = yaml.safe_load(requests.get(url).text)
        self.remote_dependencies[name] = chart_reqs["version"]

    def pull_version_from_github_pages(self, name, url):
        """Pull the version of a Helm Chart from a GitHub Pages host

        Arguments:
            name {string} -- The name of the Helm Chart
            url {string} -- The URL of the Helm Chart's GitHub Pages host
        """
        chart_reqs = yaml.safe_load(requests.get(url).text)
        updates_sorted = sorted(
            chart_reqs["entries"][name], key=lambda k: k["created"],
        )
        self.remote_dependencies[name] = updates_sorted[-1]["version"]

    def update_requirements_file(self, charts):
        """Update the requirements.yaml file of the local Helm Chart

        Arguments:
            charts {list of strings} -- List of Helm Chart names to be updated
        """
        file_path = os.path.join(HERE, self.chart, "requirements.yaml")

        with open(file_path, "r") as stream:
            chart_yaml = yaml.safe_load(stream)

        for chart in charts:
            if self.verbose:
                logging.info("Updating version for: %s" % chart)

            for dependency in chart_yaml["dependencies"]:
                if dependency["name"] == chart:
                    dependency["version"] = self.remote_dependencies[chart]

        with open(file_path, "w") as stream:
            yaml.safe_dump(chart_yaml, stream)

        if self.verbose:
            logging.info("Updated requirements in: %s" % file_path)
