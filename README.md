# Pliny

Visualizing how human knowledge changes over time by analyzing trends in the Wikipedia content library

## Developing

First, you need to create a .env file. You can just copy the .env_template file, and replace the placeholders with the actual values. Additionally, you should also install the git hooks under the git_hooks directory. To do this, just run `cp git_hooks/* .git/hooks` from the root project directory

### Python

Make sure you have both the `pylint` and `mypy type checker` extensions installed and turned on (both official from Microsoft). When you don't have any unused variables/untyped variables, it should automatically give a warning/error. It will automatically check for any linting errors before making a commit.

You will also need to create a Python venv, use at least version `3.11` to do this (can be done from the vscode command pallete).

Finally, you can run the program with `python3 ./data-pipeline/main.py` from the root project directory.
