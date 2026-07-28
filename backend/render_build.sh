#!/usr/bin/env bash

set -o errexit

pip install --upgrade pip
pip install -r backend/requirements.txt
pytest backend/tests
PYTHONPATH=. alembic -c backend/alembic.ini upgrade head