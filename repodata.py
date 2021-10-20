import subprocess

def _call(command) -> int:
    """
    Call the passed command and silence the output.
    """
    command = f"{command} > /dev/null"
    return subprocess.call(command, shell=True)

class RepoData:
    def __init__(self, name, owner):
        self.name = name # Repository name
        self.owner = owner # Repo owner
        self.num_prefixed = None # number of prefixed git commit messages
        self.num_messages = None # total
        self.sloc = None # source lines of code
        self.cc = None # cyclometric complexity
        self.func_count = None # number of function count
        
        self._complete_initialization()

    def download(self):
        """
        Download repository from Github using the Github command line.
        """
        return _call(f"gh repo clone {self.owner}/{self.name}")
        

    def _complete_initialization(self):
        """
        Set all fields based on data obtained from
        other sources.
        """

    