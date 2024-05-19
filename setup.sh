#!/bin/sh

venv_PATH="`dirname ${0}`/venv/bin/pip"

$venv_PATH install -U selenium
$venv_PATH install -U python-dotenv
$venv_PATH install -U bs4