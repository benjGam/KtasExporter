#!/usr/bin/env sh

FOLDER_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Function to add or update alias in shell config file
add_alias_to_shell_config() {
    local config_file="$HOME/$1"
    local alias_line="alias ktasexport='$FOLDER_PATH/run.sh'"

    if [ -f "$config_file" ]; then
        # Check if alias exists with different path
        local existing_alias=$(grep "alias ktasexport=" "$config_file" | cut -d "'" -f 2)
        if [ ! -z "$existing_alias" ] && [ "$existing_alias" != "$FOLDER_PATH/run.sh" ]; then
            # Create temp file for BSD/GNU sed compatibility
            temp_file=$(mktemp)
            sed "s|alias ktasexport=.*|$alias_line|" "$config_file" > "$temp_file"
            mv "$temp_file" "$config_file"
            echo "Alias 'ktasexport' path updated in $(basename "$config_file")"
        else
            if ! grep -q "$alias_line" "$config_file"; then
                printf "\n%s\n" "$alias_line" >> "$config_file"
                echo "Alias 'ktasexport' added to $(basename "$config_file")"
            else
                echo "Alias 'ktasexport' already exists in $(basename "$config_file")"
            fi
        fi
        return 0
    fi
    return 0
}

# Create virtual environment if it doesn't exist
if [ ! -d "$FOLDER_PATH/venv" ]; then
    echo "Creating virtual environment..."
    python -m venv "$FOLDER_PATH/venv/"
fi

# Install dependencies
echo "Installing dependencies..."
alias pip="$FOLDER_PATH/venv/bin/pip"
pip install -U selenium python-dotenv bs4

# Ask for alias creation
printf "\nDo you want to add the 'ktasexport' alias to your shell config? [Y/n] "
read -n 1 -s -r response
echo # New line after response

if [ "$response" = "n" ] || [ "$response" = "N" ]; then
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

echo "To use the 'ktasexport' alias in this terminal session, please run:"
echo "source ~/$( [ "$(basename "$SHELL")" = "fish" ] && echo ".config/fish/config.fish" || echo ".$(basename "$SHELL")rc" )"