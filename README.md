# helm-upgrade

⚠️ **This repository is archived and no longer actively maintained!** ⚠️

[![PyPI version](https://badge.fury.io/py/helm-upgrade.svg)](https://badge.fury.io/py/helm-upgrade) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sgibson91/helm-upgrade/main.svg)](https://results.pre-commit.ci/latest/github/sgibson91/helm-upgrade/main) [![CI Tests](https://github.com/sgibson91/helm-upgrade/actions/workflows/ci.yaml/badge.svg)](https://github.com/sgibson91/helm-upgrade/actions/workflows/ci.yaml) [![codecov](https://codecov.io/gh/sgibson91/helm-upgrade/branch/main/graph/badge.svg?token=U2HTE7X6BK)](https://codecov.io/gh/sgibson91/helm-upgrade)

Do you manage a Helm Chart that has dependencies on other Helm Charts?
Are you fed up of manually updating these dependencies?
Then this is the tool for you!
`helm-upgrade` is a Python command line interface (CLI) that automatically updates the dependencies of local Helm Charts.

This tool was inspired by [`bump-helm-deps-action`](https://github.com/sgibson91/bump-helm-deps-action).

**Table of Contents**

- [:rocket: Installation](#rocket-installation)
  - [:snake: `pip`](#snake-pip)
  - [:wrench: Manual](#wrench-manual)
- [:recycle: Usage](#recycle-usage)
  - [:wheel_of_dharma: Remote Helm Charts](#wheel_of_dharma-remote-helm-charts)
- [:white_check_mark: Running Tests](#white_check_mark-running-tests)
- [:sparkles: Contributing](#sparkles-contributing)

---

## :rocket: Installation

It's recommended to use Python version 3.8 with this tool.

### :snake: `pip`

```bash
pip install helm-upgrade
```

### :wrench: Manual

First of all, clone this repository and change into it.

```bash
git clone https://github.com/sgibson91/helm-upgrade.git
cd helm-upgrade
```

Use Python to install requirements and the package.
Python 3.8 is recommended.

```bash
python -m pip install .
```

Test the installation by calling the help page.

```bash
helm-upgrade --help
```

## :recycle: Usage

```
usage: helm-upgrade [-h] [--dry-run] chart_path dependencies

Update the dependencies of a local Helm Chart in a project repository.

positional arguments:
  chart_path    Path to the file containing the dependencies of the local Helm Chart to
                be updated.
  dependencies  A dictionary of Helm Chart dependencies and their host repo URLs. E.g.
                '{"nginx-ingress":
                "https://raw.githubusercontent.com/helm/charts/master/stable/nginx-
                ingress/Chart.yaml"}'

optional arguments:
  -h, --help    show this help message and exit
  --dry-run     Perform a dry run of the update. Don't write the changes to a file.
```

`helm-upgrade` will then:

1) read the current versions of your dependencies from the file you specify,
2) find the latest versions of your desired dependencies from the URLs provided (in JSON schema) to the `dependencies` argument,
3) compare whether these versions are equal,
4) if the versions are not equal (and the `--dry-run` flag has not been set), your helm chart dependencies will be overwritten with the new chart versions.

### :wheel_of_dharma: Remote Helm Charts

`helm-upgrade` currently recognises chart versions from three types of hosts.

1) A `Chart.yaml` file from another GitHub repository.
   These URLs end with "`/Chart.yaml`".

   For example, [https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml](https://github.com/helm/charts/blob/master/stable/nginx-ingress/Chart.yaml)

2) A repository of chart versions hosted on GitHub pages.
   These URLs contain "`/gh-pages/`".

   For example, [https://raw.githubusercontent.com/jupyterhub/helm-chart/gh-pages/index.yaml](https://github.com/jupyterhub/helm-chart/blob/gh-pages/index.yaml)

3) Versions listed on a GitHub Releases page.
   These URLs end with "`/releases/latest`" and uses `BeautifulSoup` to search the html.

   For example, <https://github.com/jetstack/cert-manager/releases/latest>

## :white_check_mark: Running Tests

To run the test suite, you must first following the [manual installation instructions](#wrench-manual).
Once completed, the test suite can be run as follows:

```bash
python -m pytest -vvv
```

To see code coverage of the test suite, run the following:

```bash
python -m coverage run -m pytest -vvv
coverage report
```

An interactive HTML version of the report can be accessed by running the following:

```bash
coverage html
```

And then opening the `htmlcov/index.html` file in a browser window.

## :sparkles: Contributing

:tada: Thank you for wanting to contribute! :tada:
Make sure to read our [Code of Conduct](CODE_OF_CONDUCT.md) and [Contributing Guidelines](CONTRIBUTING.md) to get you started.
