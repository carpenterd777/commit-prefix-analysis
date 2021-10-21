"""
Setup module to make CLI extensible.
"""

from setuptools import setup

setup(
    name='commit-prefix-analysis',
    version='1.0.0',
    py_modules=['commit-prefix-analysis.py'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'commit-prefix-analysis = commit-prefix-analysis:cli',
        ],
    },
)