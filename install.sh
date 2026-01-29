#/bin/bash

BASH_RC="$HOME/.bashrc"
CONFIG_LINE="alias todo='python3 $HOME/TODOAPP/TODOLIST.py'"

# Edit .bashrc safely
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
