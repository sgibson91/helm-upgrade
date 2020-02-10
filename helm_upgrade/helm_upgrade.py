"""Update Helm Chart dependencies."""
import os


HERE = os.path.dirname(__file__)
ABSOLUTE_HERE = os.path.dirname(os.path.realpath(__file__))


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
            logging()
