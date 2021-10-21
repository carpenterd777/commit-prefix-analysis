"""
Implement cpa command.
"""

import subprocess
import re
import click


def check_gh_installed():
    """
    Throws an Exception if the GitHub CLI is not installed.
    """
    bytes_result = subprocess.check_output("gh --version")
    result = bytes_result.decode("utf-8")
    prog = re.compile(r"gh version 2.\d.\d")

    if not prog.match(result):
        raise RuntimeError(
            f"could not find gh, got ${result} when checking the version"
        )


@click.command()
@click.argument("repositories", nargs=-1)
def main(repositories):
    """Main method."""
    try:
        check_gh_installed()
    except RuntimeError:
        print("uh oh")
