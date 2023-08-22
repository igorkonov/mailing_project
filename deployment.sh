#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py loaddata db.json
sudo service redis-server start
python3 manage.py runserver
python3 manage.py services