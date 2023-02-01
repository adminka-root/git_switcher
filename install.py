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


if __name__ == "__main__":
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # '~/.local/share/git_switcher'
    rc_file = os.path.expanduser('~/.bashrc')

    backup_file(rc_file)
    backup_file(os.path.expanduser('~/.ssh/config'))

    need_add = f"if [ -d '{ script_dir }' ]; then alias git_swither='{ script_dir }/source/git_switcher.py'; " + \
               f"alias git_swither_uninstall='{ script_dir }/uninstall.py'; fi"

    with open(rc_file, 'r+') as file:
        if need_add not in file.read():
            file.write(need_add)
