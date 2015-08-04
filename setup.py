"""Setup for LMS Manipulator XBlock."""

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
    name='lmsmanipulator-xblock',
    version='0.1',
    description='LMS Manipulator XBlock',   # TODO: write a better description.
    packages=[
        'lmsmanipulator',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'lmsmanipulator = lmsmanipulator:LMSManipulatorXBlock',
        ]
    },
    package_data=package_data("lmsmanipulator", ["static", "templates", "public"]),
)
