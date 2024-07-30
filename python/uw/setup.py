# coding: utf-8

"""
    Unnatural Worlds API
"""

from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "unnatural-worlds-api"
VERSION = "21.1.1"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
]

setup(
    name=NAME,
    version=VERSION,
    description="Unnatural Worlds Bot API",
    author="tivvit",
    author_email="tivvitmail@gmail.com",
    url="",
    keywords=["uw", "unnatural worlds"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="""\
    Unnatural Worlds Bot API
    """,  # noqa: E501
    package_data={"": ["bots.h"]},
)
