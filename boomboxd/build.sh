#!/usr/bin/env bash
set -o errexit

pip install -r ./boomboxd/requirements.txt

python ./boomboxd/manage.py collectstatic --no-input

python ./boomboxd/manage.py migrate
