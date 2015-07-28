"""Setup for AnalyticsExtras XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):

    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='analyticsextras-xblock',
    version='0.1',
    description='AnalyticsExtras XBlock',   # TODO: write a better description.
    packages=[
        'analyticsextras',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'analyticsextras = analyticsextras:AnalyticsExtrasXBlock',
        ]
    },
    package_data=package_data("analyticsextras", ["static", "templates", "public"]),
)
