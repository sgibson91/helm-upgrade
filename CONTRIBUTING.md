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
- [:gift: How can I contribute?](#gift-how-can-i-contribute)
  - [:bug: Reporting Bugs](#bug-reporting-bugs)
  - [:sparkles: Requesting Features](#sparkles-requesting-features)

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

- :question: Package information for building and distributing to PyPI is contained within `setup.py`
- :pushpin: The package dependencies are defined in `requirements.txt`
- :file_folder: The package itself is contained within the `helm_upgrade` folder
- :snake: The `HelmUpgrade` Python class is defined in `helm_upgrade.py`
- :video_game: The cli is defined in `cli.py`

### :recycle: Continuous Integration

This repository uses [GitHub Actions](https://help.github.com/en/actions) :runner: :dash: to run tests.
These are defined in the `.github/workflows` folder.
An example Helm chart `requirements.yaml` file is given in the `test-chart` folder to run tests against.

## :gift: How can I contribute?

### :bug: Reporting Bugs

If something doesn't work the way you expect it to, please check it hasn't already been reported in the repository's [issue tracker](https://github.com/sgibson91/helm-upgrade/issues).
Bug reports should have the [bug label](https://github.com/sgibson91/helm-upgrade/issues?q=is%3Aopen+is%3Aissue+label%3Abug), or have a title beginning with [[BUG]](https://github.com/sgibson91/helm-upgrade/issues?q=is%3Aissue+is%3Aopen+%5BBUG%5D).

If you can't find an issue already reporting your bug, then please feel free to [open a new issue](https://github.com/sgibson91/helm-upgrade/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D).
This repository has a [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) to help you be as descriptive as possible so we can squash that bug! :muscle:

### :sparkles: Requesting Features

If there was something extra you wish `helm-upgrade` could do, please check that the feature hasn't already been requested in the project's [issue tracker](https://github.com/sgibson91/helm-upgrade/issues).
Feature requests should have the [enhancement label](https://github.com/sgibson91/helm-upgrade/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement).
Please also check the [closed issues](https://github.com/sgibson91/helm-upgrade/issues?q=is%3Aclosed+is%3Aissue) to make sure the feature has not already been requested but the project maintainers decided against developing it.

If you find an open issue describing the feature you wish for, you can "+1" the issue by giving a thumbs up reaction on the **top comment of the issue**.
You may also leave any thoughts or offers for support as new comments on the issue.

If you don't find an issue describing your feature, please [open a feature request](https://github.com/sgibson91/helm-upgrade/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=).
This repository has a [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) to help you map out the feature you'd like.
