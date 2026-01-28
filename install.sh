#!/bin/bash

# --- Configuration ---
REPO_URL="https://github.com/NVitschDEV/TODOAPP.git"
INSTALL_DIR=""
BASH_RC="$HOME/.bashrc"
# The specific line you want to add (e.g., adding to PATH or sourcing a script)
CONFIG_LINE="alias todo='python3 $HOME/TODOAPP/TODOLIST.py'"

# --- Functions ---

print_msg() {
    echo -e "\033[1;32m[INSTALL]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# --- Main Logic ---

# 1. Check if Git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git and try again."
    exit 1
fi

# 2. Clone the Repository
if [ -d "$INSTALL_DIR" ]; then
    print_msg "Directory $INSTALL_DIR already exists. Pulling latest changes..."
    cd "$INSTALL_DIR" && git pull
else
    print_msg "Cloning $REPO_URL into $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 3. Edit .bashrc safely
if [ -f "$BASH_RC" ]; then
    # Check if the line already exists (Idempotency check)
    if grep -Fxq "$CONFIG_LINE" "$BASH_RC"; then
        print_msg "Configuration already exists in $BASH_RC. Skipping."
    else
        print_msg "Backing up $BASH_RC to $BASH_RC.bak..."
        cp "$BASH_RC" "$BASH_RC.bak"

        print_msg "Adding configuration to $BASH_RC..."
        # Add a newline just in case the file doesn't end with one
        echo "" >> "$BASH_RC"
        echo "# Added by install.sh script" >> "$BASH_RC"
        echo "$CONFIG_LINE" >> "$BASH_RC"
    fi
else
    print_error "$BASH_RC does not exist. (Are you using zsh?)"
fi

print_msg "Installation complete!"
print_msg "Please restart your terminal or run: source $BASH_RC"
