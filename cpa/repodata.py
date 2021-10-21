"""
Implements the RepoData type.
"""

import subprocess
import re
import shutil
import os
from textwrap import dedent


def _call(command) -> str:
    """
    Call the passed command and silence the output.
    """
    command = f"{command}"
    return subprocess.check_output(command, shell=True)


class RepoData:
    """
    Holds information relating to a GitHub repositorty.
    """

    def __init__(self, name, owner):
        self.name = name  # Repository name
        self.owner = owner  # Repo owner
        self.num_prefixed = None  # number of prefixed git commit messages
        self.num_messages = None  # total
        self.sloc = None  # source lines of code
        self.cyclo = None  # cyclometric complexity
        self.func_count = None  # number of function count

        self._complete_initialization()

    def __str__(self):
        return dedent(
            f"""
        {self.owner}/{self.name},{self.num_prefixed},{self.num_messages},{self.sloc},{self.cyclo},{self.func_count}
        """
        )

    def download(self):
        """
        Download repository from Github using the Github command line.
        """
        return _call(f"gh repo clone {self.owner}/{self.name}")

    def count_messages(self):
        """
        Using git, count the number of commit messages and prefixed commit messages
        on the default branch of the repository.
        """

        # Intialize
        os.chdir(f"./{self.name}")
        result = subprocess.check_output("git log --pretty=oneline", shell=True).decode(
            "utf-8"
        )
        message_list = result.splitlines()
        message_list = [
            message for message in message_list if message != ""
        ]  # Filter out blank lines

        # count each message
        self.num_messages = len(message_list)

        # remove commit hashes
        message_list = [self._remove_commit_hash(message) for message in message_list]

        # count messages with prefixes
        self.num_prefixed = 0
        for message in message_list:
            if self._is_prefixed(message):
                self.num_prefixed += 1

        # cleanup
        os.chdir("..")

    def compute_repo_complexity(self):
        """
        Computes the repo complexity and sets the
        sloc, cyclo, and function_count fields.
        """
        result = subprocess.check_output(f"lizard {self.name}", shell=True).decode(
            "utf-8"
        )
        lines = result.splitlines()
        total_line = lines[len(lines) - 1]
        totals = total_line.split()
        self.sloc = totals[0]
        self.cyclo = totals[2]
        self.func_count = totals[4]

    def cleanup(self):
        """
        Delete the repo folder that was created.
        """
        shutil.rmtree(f"./{self.name}")

    def _complete_initialization(self):
        """
        Set all fields.
        """
        self.download()
        self.count_messages()
        self.compute_repo_complexity()
        self.cleanup()

    def _is_prefixed(self, string) -> bool:
        """
        matches short, one-word prefixes

        Examples:
        feat: add foo
        chore: remove bar
        #72: give customer wombats
        refactor: something smelly

        Anti-examples: (should not match)
        hello I am some default text
        super refactor: something smellier
        you cannot just have: a colon
        """
        prog = re.compile(r"^[\S#]{1,8}:")
        return prog.match(string) is not None

    def _remove_commit_hash(self, message: str) -> str:
        """
        Removes the commit hash from a commit message string.
        """
        return " ".join(message.split()[1:])
