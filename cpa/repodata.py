"""
Implements the RepoData type.
"""

import subprocess
import re
import shutil
import lizard


def _call(command) -> int:
    """
    Call the passed command and silence the output.
    """
    command = f"{command} > /dev/null"
    return subprocess.call(command, shell=True)


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
        _call(f"cd ./${self.name}")
        result = subprocess.check_output("git log --pretty=oneline").decode("utf-8")
        message_list = result.splitlines()
        message_list = [
            message for message in message_list if message != ""
        ]  # Filter out blank lines

        # count each message
        self.num_messages = len(message_list)

        # count messages with prefixes
        self.num_prefixed = 0
        for message in message_list:
            if self._is_prefixed(message):
                self.num_prefixed += 1

        # cleanup
        _call("cd ..")

    def _complete_initialization(self):
        """
        Set all fields.
        """
        self.download()
        self.count_messages()
        self.compute_repo_complexity()
        self.cleanup()

    def compute_repo_complexity(self):
        """
        Computes the repo complexity and sets the
        sloc, cyclo, and function_count fields.
        """
        info = lizard.analyze(f"./{self.name}")
        self.sloc = info.__dict__["nloc"]
        self.cyclo = info.__dict__["cyclomatic_complexity"]
        self.func_count = len(info.__dict__["function_list"])

    def cleanup(self):
        """
        Delete the repo folder that was created.
        """
        shutil.rmtree(f"./${self.name}")


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
