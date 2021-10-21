"""
Setup module to make CLI extensible.
"""

from setuptools import setup

setup(
    name='cpa',
    version='1.0.0',
    py_modules=['cpa'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cpa = cpa:cli',
        ],
    },
)