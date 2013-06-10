#!/usr/bin/env python
from setuptools import setup, find_packages

LONGDESCRIPTION = """ pymcm-deckbox is a library for interacting with web https://www.magiccardmarket.eu/ and http://www.deckbox.org.
For example, you can calculate the MCM card value of the required cards of a deck."""

setup(
    name="pymcm-deckbox",
    version="0.0.3",
    description="MagicCardMarket API client applied to decklists from Deckbox.org",
    long_description=LONGDESCRIPTION,
    license="MIT",
    install_requires=["lxml", "mechanize"],
    author="Stefan Frijters",
    author_email="sfrijters@gmail.com",
    url="http://github.com/SFrijters/pymcm-deckbox",
    packages=find_packages(),
    keywords="mcm",
    zip_safe=True
)
