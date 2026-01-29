#!/bin/bash

# --- Variables ---
APP_DIR="$HOME/TODOAPP"
BASH_RC="$HOME/.bashrc"
# We reconstruct the exact line used in the install script to ensure a match
CONFIG_LINE="alias todo='python3 $APP_DIR/TODOLIST.py'"
MARKER_LINE="# Added by install.sh script"

# --- Helper Functions ---
print_msg() { echo -e "\033[1;32m[INFO]\033[0m $1"; }
print_warn() { echo -e "\033[1;33m[WARN]\033[0m $1"; }
print_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# --- Main Logic ---

# 1. Clean up .bashrc
if [ -f "$BASH_RC" ]; then
    # Check if the config actually exists before trying to edit
    if grep -Fq "$CONFIG_LINE" "$BASH_RC"; then
        print_msg "Configuration found in $BASH_RC."

        # Create a backup before modifying
        print_msg "Backing up $BASH_RC to $BASH_RC.uninstall.bak..."
        cp "$BASH_RC" "$BASH_RC.uninstall.bak"

        print_msg "Removing configuration lines..."
        # Use grep -v (inverse match) to create a temp file without the specific lines
        # -F ensures we treat the string as a fixed string, not a regex (safe for file paths)
        grep -vF "$CONFIG_LINE" "$BASH_RC" | grep -vF "$MARKER_LINE" > "$BASH_RC.tmp"

        # Overwrite original file
        mv "$BASH_RC.tmp" "$BASH_RC"
        print_msg "Successfully cleaned $BASH_RC."
    else
        print_warn "Configuration line not found in $BASH_RC. Skipping file edit."
    fi
else
    print_error "$BASH_RC not found."
fi

# 2. Remove the Application Directory
if [ -d "$APP_DIR" ]; then
    echo "Removing application directory: $APP_DIR"
    rm -rf "$APP_DIR"
else
    echo "Directory $APP_DIR does not exist or was already removed."
fi

# 3. Final Instructions
echo "--------------------------------------------------------"
echo "Uninstallation complete."
echo "Please restart your terminal or run the following command to apply changes:"
echo "source ~/.bashrc && unalias todo 2>/dev/null"
