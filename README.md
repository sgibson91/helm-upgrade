# helm-upgrade

[![PyPI version](https://badge.fury.io/py/helm-upgrade.svg)](https://badge.fury.io/py/helm-upgrade)

| | Status |
| :--- | :--- |
| CI Tests | ![GitHub Actions - CI Tests](https://github.com/sgibson91/helm-upgrade/workflows/CI-test/badge.svg) |
| Black | ![GitHub Actions - Black](https://github.com/sgibson91/helm-upgrade/workflows/Black/badge.svg) |
| Flake8 | ![GitHub Actions - Flake8](https://github.com/sgibson91/helm-upgrade/workflows/Flake8/badge.svg) |

Do you manage a Helm Chart that has dependencies on other Helm Charts?
Are you fed up of manually updating these dependencies?
Then this is the tool for you!
`helm-upgrade` is a Python command line interface (CLI) that automatically updates the dependencies of local Helm Charts.

This tool was inspired by [HelmUpgradeBot](https://github.com/HelmUpgradeBot/hub23-deploy-upgrades) and [Chris Holdgraf's github-activity tool](https://github.com/choldgraf/github-activity).

- [Installation](#installation)
  - [`pip`](#pip)
  - [Manual](#manual)
- [Usage](#usage)
  - [Remote Helm Charts](#remote-helm-charts)

---

## Installation

It's recommended to use Python version 3.7 with this tool.

### `pip`

```bash
pip install helm-upgrade
```

### Manual

First of all, clone this repository and change into it.

```bash
git clone https://github.com/sgibson91/helm-upgrade.git
cd helm-upgrade
```

Use Python to install requirements and the package.
Python 3.7 is recommended.

```bash
python -m pip install -r requirements.txt
python setup.py install
```

Test the installation by calling the help page.

```bash
helm-upgrade --help
```

## Usage

```
usage: helm-upgrade [-h] [--dry-run] [-v] chart dependencies

Update the dependencies of a local Helm Chart in a project repository.

positional arguments:
  chart          Name of the local Helm Chart to be updated
  dependencies   A dictionary of Helm Chart dependencies and their host repo URLs.
                 For example, '{"nginx-ingress": "https://raw.githubusercontent.com/helm/charts/master/stable/nginx-ingress/Chart.yaml"}'

optional arguments:
  --dry-run      Perform a dry run of the update. Don't write the changes to a file.
  -v, --verbose  Option to turn on logging.
```

Run the CLI in the directory _above_ your local helm chart.
For example:

```bash
$ ls -R -1

./my-local-helm-chart:
Chart.yaml
README.md
requirements.yaml
templates/
values.yaml
```

In this example, the `name` argument would be `my-local-helm-chart`.

`helm-upgrade` will then:

1) read the current versions of your dependencies from your `requirements.yaml` file,
2) find the latest versions of your desired dependencies from the URLs provided (in JSON schema) to the `dependencies` argument,
3) compare whether these versions are equal,
4) if the versions are not equal (and the `--dry-run` flag has not been set), `requirements.yaml` will be overwritten with the new chart versions.

The `--verbose` flag will print logs to the console and the `--dry-run` flag will skip the file writing step.

### Remote Helm Charts

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
