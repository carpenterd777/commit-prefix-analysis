# commit-prefix-analysis

Script to quickly get the metrics from Github repos to analyze.

## Setup

Install the [Github CLI](https://cli.github.com/). You'll know its working when running `gh --version` returns a version number.

Create a Python virtual environment. Run:

```bash
python3 -m venv .venv
```

Then activate your virtual environment:

```bash
source .venv/bin/activate
# on Windows
.venv/Scripts/Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Finally, build the command in your virtual environment:

```bash
pip install --editable cpa
```

You'll know you've got it working when `cpa --version` returns a usage message.

## Usage

```bash
cpa [...repositories]
```

Example:
```bash
cpa carpenterd777/commit-prefix-analysis

# Another example
cpa carpeterd777/commit-prefix-analysis elenirotsides/Trivia-Bot
```

You can add any number of repositories as an argument to the command, as long as they are in the form `owner/name`.

Creates a .csv file `results.csv` in the directory in which it was run.

⚠ This command creates and deletes directories in the current working directory where it is called. This could cause problems if there are other directories with the same name as the repos being downloaded. It is advised to run this in an empty directory. ⚠

## Teardown

When you're finished with the script run `deactivate` to leave the Python virtual environment.

## More Info

To learn more about what a virtual environement in Python is, read here: [Create a Python virtual environment using venv](https://cloudbytes.dev/articles/create-a-python-virtual-environment-using-venv)