"""setup.py for pt-variant-a (Variant A - Detectable - Wheel version).

For Artifactory deployment: Build wheel with embedded payload code.
Payload executes on package import via __init__.py
"""
from setuptools import setup, find_packages

setup(
    name='pt-variant-a',
    version='1.1.0',
    description='Utility package for PT applications (variant A)',
    author='purple-team',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
)
