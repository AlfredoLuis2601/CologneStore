#!/usr/bin/env bash

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Roda as migrações do banco de dados antes de subir o app
alembic upgrade head