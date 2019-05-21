# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup

# Should equal quasardb api version
version = "3.3.2"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="qdb-prometheus-exporter",
    packages=["qdb_prometheus_exporter"],
    entry_points={
        "console_scripts": ['qdb-prometheus-exporter = qdb_prometheus_exporter.exporter:main']
    },
    version=version,
    author="Mickaël GERVAIS",
    author_email="mgervais@agaetis.fr",
    description="Command line utility to export QuasarDB metricsto Prometheus.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "prometheus_client",
        "quasardb >= 3.3.2"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Programming Language :: Python :: Implementation',

        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Monitoring Tools',
    ],
    keywords='QuasarDB Prometheus'

)
