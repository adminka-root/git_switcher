#!/usr/bin/env python3

import os
import subprocess


if __name__ == "__main__":
    script_dir = os.path.expanduser('~/.local/share/git_switcher/')
    user_environment_dir = os.path.expanduser('~/.local/bin')

    dest = os.path.join(user_environment_dir, 'git_switcher_uninstall')
    if os.path.exists(dest) or os.path.islink(dest):
        os.remove(dest)

    dest = os.path.join(user_environment_dir, 'git_switcher')
    if os.path.exists(dest) or os.path.islink(dest):
        os.remove(dest)

    subprocess.Popen(
"""
python -c
\"import shutil, time;
time.sleep(1);
shutil.rmtree('{}');\"
""".format(script_dir).replace('\n', ' '),
        shell=True
    )
