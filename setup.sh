#!/bin/sh

FOLDER_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Function to add or update alias in shell config file
add_alias_to_shell_config() {
    local config_file="$HOME/$1"
    local alias_line="alias ktasexport='$FOLDER_PATH/run.sh'"

    if [ -f "$config_file" ]; then
        # Check if alias exists with different path
        local existing_alias=$(grep "alias ktasexport=" "$config_file" | cut -d "'" -f 2)
        if [ ! -z "$existing_alias" ] && [ "$existing_alias" != "$FOLDER_PATH/run.sh" ]; then
            sed -i "s|alias ktasexport=.*|$alias_line|" "$config_file"
            echo "Alias 'ktasexport' path updated in $(basename "$config_file")"
        else
            if ! grep -q "$alias_line" "$config_file"; then
                echo "" >> "$config_file"
                echo "$alias_line" >> "$config_file"
                echo "Alias 'ktasexport' added to $(basename "$config_file")"
            fi
        fi
        return 0
    fi
    return 0
}

python -m venv $FOLDER_PATH/venv/

# Has to be improved
# - Add other shell rc aliases
# - Add question on adding alias
# - Add auto source on rc file
# - Add way to auto update alias if run file is not at defined path

alias pip="$FOLDER_PATH/venv/bin/pip"

pip install -U selenium
pip install -U python-dotenv
pip install -U bs4

echo "Do you want to add the 'ktasexport' alias to your shell config? (Y/n)"
read ADD_ALIAS

if [ "$ADD_ALIAS" = "n" ] || [ "$ADD_ALIAS" = "N" ]; then
    exit 0
fi

# Shell config files to process
SHELL_CONFIGS=(
    ".zshrc"
    ".bashrc"
    ".config/fish/config.fish"
)

# Try to add alias to all shell configs
for config in "${SHELL_CONFIGS[@]}"; do
    add_alias_to_shell_config "$config"
done