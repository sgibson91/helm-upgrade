# Contributing Guidelines

:space_invader: :tada: Thank you for contributing to the `helm-upgrade` project! :tada: :space_invader:

The following is a set of guidelines for contributing to `helm-upgrade` on GitHub.
These are mostly guidelines, not rules.
Use your best judgement and feel free to propose changes to this document in a Pull Request.

**Table of Contents**

- [:purple_heart: Code of Conduct](#purple_heart-code-of-conduct)
- [:question: What should I know before I get started?](#question-what-should-i-know-before-i-get-started)
  - [:package: `helm-upgrade`](#package-helm-upgrade)
  - [:recycle: Continuous Integration](#recycle-continuous-integration)

---

## :purple_heart: Code of Conduct

This project and everyone participating in it is expected to abide by and uphold the [Code of Conduct](CODE_OF_CONDUCT.md).
Please report any unacceptable behaviour to [drsarahlgibson@gmail.com](mailto:drsarahlgibson@gmail.com).

## :question: What should I know before I get started?

### :package:  `helm-upgrade`

`helm-upgrade` is a [Python package](https://packaging.python.org/overview/) and Command Line Interface (cli) tool that manages the dependencies of [Helm charts](https://helm.sh/).
It takes the name of a local Helm chart and a dictionary of dependent chart names (as keys) and the URL documenting their version history (as values) as input.

When executed, `helm-upgrade` will read in the versions of dependent charts from the local `requirements.yaml` file.
It will then pull the latest versions of these charts from the URL provided on the command line.
If the two versions do not match, `helm-upgrade` will overwrite `requirements.yaml` with the new version.

There are also optional command line flags for verbose output and to perform a dry run (`requirements.yaml` will not be overwritten).

- :file_folder: The package is contained within the `helm_upgrade` folder
- :snake: The `HelmUpgrade` Python class is defined in `helm_upgrade.py`
- :video_game: The cli is defined in `cli.py`

### :recycle: Continuous Integration
