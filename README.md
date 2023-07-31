# Qvik Challenge - Backend Dev Position

## Overview
Simple Rest API (Backend) to serve data of different news articles under different channels (Science, Sports, etc).

Tech stack: Python, FastAPI, SQLalchemy, SQLite.

Features include:

- CRUD operations for articles and channels.
- Store data including article info, channel info, article url and word count in a SQLite database. 
- Search articles with word count ranges (0-100), (100-500) and (0-501).


## Running Locally
The solution has been written and tested with Python version 3.8.10.

If you want to setup the virtual environment first, please make sure python3.8-venv is installed or install it by running:

`sudo apt install python3.8-venv`

then run:

`python3 -m venv .venv`

and activate the virtual env:

`source .venv/bin/activate`

  
To setup the solution, please install the dependencies by running: `pip install -r requirements.txt`, preferably inside a virtual env to avoid conflicts.

You can use the script `api_start.sh` to run the application from the terminal, which will start the API on `localhost:8000`. The API docs are available at the endpoint `/docs`, which can also be used to send requests to the API and also shows a sample curl request.

Tests can be also run by using the following command:

`python -m pytest tests/`
