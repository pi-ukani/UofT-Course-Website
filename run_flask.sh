#!/bin/bash
source venv/bin/activate
sleep 2
export FLASK_ENV=development
export FLASK_APP=app.py
flask run