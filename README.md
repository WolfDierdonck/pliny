# Pliny

Visualizing how human knowledge changes over time by analyzing trends in the Wikipedia content library.

As part of this project, there are three main components all in this repo:

1. The data pipeline. This queries the WikiMedia APIs and processes it for the visualizations
2. The backend. This queries the processed data and returns it to the frontend.
3. The frontend. This visualizes the data.

## Developing

First, you need to create a .env file. You can just copy the .env_template file, and replace the placeholders with the actual values. Note that you will also need to add any JSON files containing secrets to a new `secrets` directory. Additionally, you should also install the git hooks under the git_hooks directory. To do this, just run `cp git_hooks/* .git/hooks` from the root project directory.

### Data Pipeline (Python)

All of the code for this component is inside the `data-pipeline` folder.

Make sure you have both the `pylint` and `mypy type checker` extensions installed and turned on (both official from Microsoft). When you don't have any unused variables/untyped variables, it should automatically give a warning/error. It will automatically check for any linting errors before making a commit.

You will also need to create a Python venv, use at least version `3.11` to do this (can be done from the vscode command pallete).

Finally, you can run the program with `python3 ./data-pipeline/main.py` from the root project directory.

### Backend (Go)

All of the code for this component is in the `backend` folder.

Make sure you have Go installed, the version used to develop this is `1.23.3`. Also make sure you have the Go extension in VSCode installed for linting/etc.

You'll need to install the Go dependencies with `go get .` inside the `backend` folder. Then, you can run the backend using `go run *.go` and it'll run on localhost:8080.

### Frontend (TypeScript)

All of the code for this component is inside the `frontend` folder.

Make sure you have both the `ESLint` and `Prettier` extensions installed and enabled. These will detect any linting/formatting issues and give errors for them. It's a good idea to also have prettier auto-format on save.

Then, you'll need to install all the dependencies using `npm i` inside the `frontend` folder. Note this should be done every time you pull new changes and a new package is added.

Finally, you can run the webapp using `npm start` and it'll run on localhost:3000.
