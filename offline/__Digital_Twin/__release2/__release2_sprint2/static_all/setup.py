# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

from setuptools import setup, find_packages

setup(
    # Expecting rrps.dt.integrator to be namespace, particular integrators within
    name='rrps.dt.integrator',
    description='RRPS Integrator',
    version='0.1.8',
    author='RRPS',
    author_email='info@rrps.nowhere',
    url='https://rrps.nowhere',
    packages=find_packages(),
    zip_safe=True,
    python_requires='>=3.6',
    install_requires=[
        'ioticlabs.dt.common>=0.1.3,<0.2',
        'ioticlabs.dt.api>=0.1.7,<0.2',
        'rrps.dt.events>=0.1.7,<0.2',
        'ioticlabs.common.storeutil>=0.1.0,<0.2',
        'requests>=2.19.1,<3'
    ],
    entry_points={
        'console_scripts': [
            'rrps-dt-integrator-talendfirmware = rrps.dt.integrator.talendfirmware.__main__:main'
            'rrps-dt-integrator-talendtimdocument = rrps.dt.integrator.talendtimdocument.__main__:main'
        ]
    }
)
