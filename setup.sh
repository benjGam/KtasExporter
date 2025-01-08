#!/bin/sh

FOLDER_PATH=`dirname ${0}`

python -m venv $FOLDER_PATH/venv/

# Has to be improved
# - Add other shell rc aliases
# - Add question on adding alias
# - Add auto source on rc file
# - Add way to auto update alias if run file is not at defined path

if [ -f "$HOME/.zshrc" ]; then
  echo "
alias ktasexport='`pwd`/run.sh'" >> "$HOME/.zshrc"
fi

alias pip="$FOLDER_PATH/venv/bin/pip"

pip install -U selenium
pip install -U python-dotenv
pip install -U bs4