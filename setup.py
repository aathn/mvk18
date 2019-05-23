from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="skysensestreamer",
    version="0.1.0",
    description="Stream video of passing aircrafts with camera module connected to Skysense v2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MVK Group 10",
    author_email="mwesslen@kth.se",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages("skysensestreamer"),
    python_requires=">=3.5",
    install_requires=["numpy", "maestro>=0.1.0"],
    dependency_links=["git+https://github.com/m4reko/maestro#egg=maestro-0.1.0"],
    include_package_data=True,
    package_data={"": ["conf.ini"]},
)
