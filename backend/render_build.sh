#!/usr/bin/env bash

set -o errexit

pip install --upgrade pip
pip install -r backend/requirements.txt
PYTHONPATH=. alembic -c backend/alembic.ini upgrade head