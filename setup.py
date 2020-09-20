#!/usr/bin/env python

import pathlib

import setuptools
import toml

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

pyproject_toml = (here / 'pyproject.toml').read_text()
pyproject_data = toml.loads(pyproject_toml)

setuptools.setup(**pyproject_data['project'])
