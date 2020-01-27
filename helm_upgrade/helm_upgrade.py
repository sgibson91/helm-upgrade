"""Use GitHub API to update Helm Chart dependencies."""


def logging():
    """Enable logging configuration."""
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        filename="helm_upgrade.log",
        filemode="a",
        format="[%(asctime)s %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class HelmUpgrade:
    """
    HelmUpgrade class for interacting with the GitHub API and making changes to
    a Helm Chart requirements file.

    Attributes:
        target_repo (str): GitHub organisation/repo containing a Helm Chart
        chart (str): The Helm Chart name
        dependencies (dict): A dictionary of helm chart dependencies and their
                             repos
        token (str): GitHub access token
        branch (str): Name of git branch to commit to
        dry_run (Bool): Whether the changes should be pushed or not
        verbose (Bool): Whether to turn on logging or not
        repo_api (str): the API URL for the target repo
    """

    def __init__(self, argsDict):
        """The constructor for HelmUpgrade class.

        Arguments:
            argsDict {dict} -- A dictionary of values parsed from argparse.
        """
        for k, v in argsDict.items():
            setattr(self, k, v)

        # Set the repo API
        self.repo_api = f"https://api.github.com/repos/{argsDict['target_repo']}/"

        # Remove any existing forks
        self.remove_fork()

        # Get the GitHub access token
        if self.token is None:
            self.get_token()

        # Turn on logging
        if self.verbose:
            logging()
