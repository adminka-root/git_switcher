#!/usr/bin/env python3
import os
import sys
import shutil
from datetime import datetime

def backup_file(file):
    if os.path.isfile(file):
        backup_postfix = datetime.now().strftime("%d_%m_%y_(%H:%M:%S)")
        save_to = file + '_' + backup_postfix + '.bak'
        shutil.copyfile(file, save_to)

def add_to_rc_file(file_path, content):
    if os.path.isfile(file_path):
        with open(file_path, 'r+') as file:
            if content not in file.read():
                file.write(content)

if __name__ == "__main__":
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # '~/.local/share/git_switcher'
    
    # List of common shell configuration files
    rc_files = [
        '~/.bashrc',
        '~/.zshrc',
        '~/.bash_profile',
        '~/.profile',
        '~/.login',
        '~/.zprofile'
    ]

    # Backup and modify each existing rc file
    for rc_file in rc_files:
        rc_file_path = os.path.expanduser(rc_file)
        if os.path.isfile(rc_file_path):
            backup_file(rc_file_path)
            
            need_add = f"\nif [ -d '{ script_dir }' ]; then\n" \
                       f"    alias git_switcher='{ script_dir }/source/git_switcher.py'\n" \
                       f"    alias git_switcher_uninstall='{ script_dir }/uninstall.py'\n" \
                       f"fi\n"
            
            add_to_rc_file(rc_file_path, need_add)

    # Backup SSH config
    backup_file(os.path.expanduser('~/.ssh/config'))
