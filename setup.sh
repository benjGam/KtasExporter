#!/bin/sh

FOLDER_PATH=`dirname ${0}`

python -m venv $FOLDER_PATH/venv/

if [ -f "$HOME/.zshrc" ]; then
  echo "
alias ktasexport='`pwd`/run.sh'" >> "$HOME/.zshrc"
fi

alias pip="$FOLDER_PATH/venv/bin/pip"

pip install -U selenium
pip install -U python-dotenv
pip install -U bs4