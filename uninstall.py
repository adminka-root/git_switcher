#!/usr/bin/env python3

import os
import re
import shutil

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read {file_path}: {str(e)}")
        return None

def write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Failed to write to {file_path}: {str(e)}")
        return False

def find_and_remove_aliases(rc_file):
    content = read_file(rc_file)
    if content is None:
        return None, None

    # Patterns for both sh-like and csh-like syntaxes
    sh_pattern = re.compile(r"if \[ -d '(.*?)' \]; then\s*alias git_switcher='.*?'\s*alias git_switcher_uninstall='.*?'\s*fi", re.DOTALL)
    csh_pattern = re.compile(r"if \( -d '(.*?)' \) then\s*alias git_switcher '.*?'\s*alias git_switcher_uninstall '.*?'\s*endif", re.DOTALL)

    sh_match = sh_pattern.search(content)
    csh_match = csh_pattern.search(content)

    if sh_match:
        script_dir = sh_match.group(1)
        new_content = sh_pattern.sub('', content)
    elif csh_match:
        script_dir = csh_match.group(1)
        new_content = csh_pattern.sub('', content)
    else:
        return None, content

    return script_dir, new_content

def main():
    default_shell = os.path.basename(os.environ.get('SHELL', ''))
    
    if default_shell in ['bash', 'sh']:
        rc_files = ['~/.bashrc']
    elif default_shell == 'zsh':
        rc_files = ['~/.zshrc']
    elif default_shell in ['csh', 'tcsh']:
        rc_files = ['~/.cshrc']
    else:
        print(f"Unsupported shell: {default_shell}")
        return

    script_dir = None
    
    for rc_file in rc_files:
        rc_path = os.path.expanduser(rc_file)
        if os.path.exists(rc_path):
            script_dir, new_content = find_and_remove_aliases(rc_path)
            if script_dir:
                print(f"Found git_switcher installation in {rc_path}")
                if write_file(rc_path, new_content):
                    print(f"Removed git_switcher aliases from {rc_path}")
                break
    
    if script_dir:
        print(f"Removing installation directory: {script_dir}")
        try:
            shutil.rmtree(script_dir)
            print("Successfully removed the installation directory.")
        except Exception as e:
            print(f"Failed to remove directory {script_dir}: {str(e)}")
    else:
        print("Could not find git_switcher installation in RC file.")
    
    print("\nUninstallation process complete.")
    print("Please restart your terminal or source your RC file to apply changes.")

if __name__ == "__main__":
    main()