#!/bin/sh

mkdir .env
cp scripts/templates/_env_template .env/local

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py db init
