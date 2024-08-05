#! /usr/bin/env bash

source ./app/venv/bin/activate

# Let the DB start
python3 app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python3 app/initial_data.py