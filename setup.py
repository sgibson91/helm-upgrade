import io
import os

from setuptools import find_packages, setup

# Package meta-data.
AUTHOR = "Sarah Gibson"
DESCRIPTION = (
    "A Python package for updating the dependencies of a local Helm Chart"  # noqa: E501
)
EMAIL = "drsarahlgibson@gmail.com"
LICENSE = "MIT"
LICENSE_TROVE = "License :: OSI Approved :: MIT License"
NAME = "helm-upgrade"
REQUIRES_PYTHON = ">=3.7.0"
URL = "https://github.com/sgibson91/helm-upgrade"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "bs4",
    "numpy",
    "pytest",
    "pyyaml",
    "requests",
]

# What packages are optional?
EXTRAS = {}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for
#  that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),  # noqa: E501
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    ext_modules=[],
    entry_points={"console_scripts": ["helm-upgrade = helm_upgrade.cli:main"]},
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        LICENSE_TROVE,
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
