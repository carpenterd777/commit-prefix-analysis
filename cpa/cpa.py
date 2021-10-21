"""
Implement cpa command.
"""

import subprocess
import re
import click
from repodata import RepoData


def check_gh_installed():
    """
    Throws an Exception if the GitHub CLI is not installed.
    """
    bytes_result = subprocess.check_output("gh --version", shell=True)
    result = bytes_result.decode("utf-8")
    prog = re.compile(r"gh version 2.\d.\d")

    if not prog.match(result):
        raise click.ClickException(
            f"could not find gh, got ${result} when checking the version"
        )


def parse_repository(repository: str):
    """
    Get the owner and name from the user input.
    """
    ownerandname = repository.split("/")
    if len(ownerandname) < 2:
        raise click.ClickException("repository must be in format owner/name")
    return (ownerandname[0], ownerandname[1])


@click.command()
@click.argument("repositories", nargs=-1)
def cli(repositories):
    """Main method."""
    check_gh_installed()

    owner, name = parse_repository(repositories[0])
    repodata = RepoData(name, owner)
    click.echo(str(repodata))
