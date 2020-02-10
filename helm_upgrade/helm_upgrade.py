"""Update Helm Chart dependencies."""
import os
import yaml
import logging
import requests


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
    """
    HelmUpgrade class for interacting with the Helm Chart repos and making
    changes to a local Helm Chart requirements file.

    Attributes:
        chart (str): The Helm Chart name
        dependencies (dict): A dictionary of helm chart dependencies and their
                             repos
        dry_run (Bool): Whether the changes should be pushed or not
        verbose (Bool): Whether to turn on logging or not
    """

    def __init__(self, argsDict):
        """The constructor for HelmUpgrade class.

        Arguments:
            argsDict {dict} -- A dictionary of values parsed from argparse.
        """
        for k, v in argsDict.items():
            setattr(self, k, v)

        # Turn on logging
        if self.verbose:
            logging_config()

    def get_local_chart_versions(self):
        """Get the versions of the chart dependencies the local chart is
        currently pulling.
        """
        self.local_dependencies = {}

        filepath = os.path.join(HERE, self.chart, "requirements.yaml")

        if self.verbose:
            logging.info(
                "Reading local chart dependencies from: %s" % filepath
            )

        with open(filepath, "r") as stream:
            chart_deps = yaml.safe_load(stream)

        for dependency in chart_deps["dependencies"]:
            self.local_dependencies[dependency["name"]] = dependency["version"]

    def get_remote_chart_versions(self):
        """Get the most recent version of the chart dependencies from the
        remote helm repository.
        """
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
                    name=dependency,
                    url=self.dependencies[dependency],
                )

    def pull_version_from_chart_file(self, name, url):
        """Function to pull the version of a Helm Chart from it's Chart.yaml
        file.

        Arguments:
            url {string} -- The URL of the Helm Chart's Chart.yaml file.
        """
        chart_reqs = yaml.safe_load(requests.get(url).text)
        self.remote_dependencies[name] = chart_reqs["version"]
