from setuptools import find_packages
from setuptools import setup

__version__ = "0.1"

setup(
    name="bpmn_redrawer", version=__version__, packages=find_packages(exclude=["tests"])
)
