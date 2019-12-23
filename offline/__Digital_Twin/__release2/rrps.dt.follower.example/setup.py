# Copyright (c) 2018 Iotic Labs Ltd. All rights reserved.

from setuptools import setup, find_packages

setup(
    # Expecting acmecorp.dt.follower to be namespace, particular followers within
    name='rrps.dt.follower.example',
    description='ACME Corporation example follower',
    version='0.1.2',
    author='Acme Corporation',
    author_email='info@acme-corp.nowhere',
    url='https://acme-corp.nowhere',
    packages=find_packages(),
    zip_safe=True,
    python_requires='>=3.6',
    install_requires=[
        'ioticlabs.common.storeutil>=0.1.0,<0.2',
        # Example: For using asset offset tracker's mongodb implementation (in ioticlabs.dt.api.follower.tracker)
        'ioticlabs.dt.common[azure]',
        'ioticlabs.dt.api>=0.1.11,<0.2',
        # Note: Minor version changes in event definitions should never break existing events, only add new versions
        # (but keep old defaults).
        'rrps.dt.events>=0.1.0,<0.2'
    ],
    entry_points={
        'console_scripts': [
            'rrps-dt-follower-example = rrps.dt.follower.example.__main__:main'
        ]
    }
)
