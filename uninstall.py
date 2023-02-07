#!/usr/bin/env python3

import os
# import sys
import subprocess

def read_file(read_from: str):
    try:
        with open(read_from, mode='r') as file:
            return file.read()
    except:
        raise Exception('Failed to read %s!' % read_from)

def save_file(save_to: str, content: str, save_mode='w'):
    try:
        with open(save_to, mode=save_mode) as file:
            file.write(content)
    except:
        raise Exception('Failed to load %s!' % save_to)


if __name__ == "__main__":
    # script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # perhaps dangerous
    script_dir = os.path.expanduser('~/.local/share/git_switcher')
    rc_file = os.path.expanduser('~/.bashrc')

    need_add = f"if [ -d '{ script_dir }' ]; then alias git_switcher='{ script_dir }/source/git_switcher.py'; " + \
               f"alias git_switcher_uninstall='{ script_dir }/uninstall.py'; fi"

    rc_file_data = read_file(rc_file)
    if need_add in rc_file_data:
        save_file(rc_file, rc_file_data.replace(need_add, ''))


    subprocess.Popen(
"""
python3 -c
\"import shutil, time;
time.sleep(1);
shutil.rmtree('{}');\"
""".format(script_dir).replace('\n', ' '),
        shell=True
    )
