#!/bin/sh

alias pip="`dirname ${0}`/venv/bin/pip"

pip install -U selenium
pip install -U python-dotenv
pip install -U bs4