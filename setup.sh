#!/bin/sh

FOLDER_PATH=`dirname ${0}`

python -m venv $FOLDER_PATH/venv/

alias pip="$FOLDER_PATH/venv/bin/pip"

pip install -U selenium
pip install -U python-dotenv
pip install -U bs4