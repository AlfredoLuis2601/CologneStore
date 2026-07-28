#!/usr/bin/env bash

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
pytest
alembic -c backend/alembic.ini upgrade head