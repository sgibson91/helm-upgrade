from setuptools import setup, find_packages

from helm_upgrade import __version__

# Source dependencies from requirements.txt file.
with open("requirements.txt", "r") as f:
    lines = f.readlines()
    install_packages = [line.strip() for line in lines]

setup(
    name="helm_upgrade",
    version=__version__,
    install_requires=install_packages,
    include_package_data=True,
    python_requires=">=3.7",
    author="Sarah Gibson",
    author_email="drsarahlgibson@gmail.com",
    url="https://sgibson91.github.io/",
    # this should be a whitespace separated string of keywords, not a list
    keywords="development helm dependencies",
    description="Update the dependencies of a helm chart to the latest published versions.",  # noqa: E501
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    use_package_data=True,
    entry_points={"console_scripts": ["helm-upgrade = helm_upgrade.cli:main"]},
)
