# Pliny

Visualizing how human knowledge changes over time by analyzing trends in Wikipedia metadata.

You can view a variety of visualizations showing off various trends at [pliny.wiki](https://pliny.wiki). This is an example of one of the trends:
<img width="933" alt="Screenshot 2025-03-24 at 5 24 54 PM" src="https://github.com/user-attachments/assets/e972bde8-de44-4193-a890-bf894917371c" />

## Overview

As part of this project, there are three main components all in this repo:

1. The data pipeline. This queries the WikiMedia APIs or data dumps and processes it for the visualizations
2. The backend. This queries the processed data and returns it to the frontend.
3. The frontend. This visualizes the data.

## Developing

During development, this project used a private BigQuery account to store all the data. If you want to upload to your own BigQuery project, you'll need to add the credentials to your local repo and create a .env file. Besides that, no additional setup should be needed.

### Data Pipeline (Python)

All of the code for this component is inside the `data-pipeline` folder.

You will need to create a Python venv, use at least version `3.11` to do this. Then, install all the requirements from `requirements.txt`

Finally, you can run the program with `python3 ./data-pipeline/main.py` from the root project directory. Note that this takes in arguments to specify what to process. You can learn about all the arguments by using `--help`. Additional details about all the various data sources available are in the `data-pipeline/README.md`.

### Backend (Go)

All of the code for this component is in the `backend` folder.

Make sure you have Go installed, the version used to develop this is `1.23.3`. 

You'll need to install the Go dependencies with `go get .` inside the `backend` folder. Then, you can run the backend using `go run *.go` and it'll run on localhost:8080.

### Frontend (TypeScript)

All of the code for this component is inside the `frontend` folder.

You'll need to install all the dependencies using `npm i` inside the `frontend` folder. Then, you can run the webapp using `npm start` and it'll run on localhost:3000.
