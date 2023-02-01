#!/usr/bin/env python3

import os
import sys

def create_dir(directory: str, mode: str):
    mode = int(mode, base=8)
    if os.path.isdir(directory):
        os.chmod(directory, mode)
    else:
        os.makedirs(directory, mode)


if __name__ == "__main__":
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))  # '~/.local/share/git_switcher/'
    os.chmod(script_dir, 448)  # 700

    # add in env
    user_environment_dir = os.path.expanduser('~/.local/bin')
    create_dir(user_environment_dir, mode='755')
    if user_environment_dir not in os.environ['PATH'].split(':'):
        need_add = '\n' + 'if [ -d "$HOME/.local/bin" ] ; then PATH="$HOME/.local/bin:$PATH"; fi'
        profile = os.path.expanduser('~/.profile')
        with open(profile, 'a') as file:
            file.write(need_add)
        print('Please execute this command to update the $PATH:\nsource ~/.profile')

    # chmod and ln -s
    dest = os.path.join(user_environment_dir, 'git_switcher_uninstall')
    if os.path.exists(dest) or os.path.islink(dest):
        os.remove(dest)
    src = os.path.join(script_dir, 'uninstall.py')
    os.chmod(src, 448)  # help if broken link
    os.symlink(src, dest)

    dest = os.path.join(user_environment_dir, 'git_switcher')
    if os.path.exists(dest) or os.path.islink(dest):
        os.remove(dest)
    src = os.path.join(script_dir, 'source', 'git_switcher.py')
    os.chmod(src, 448)
    os.symlink(src, dest)
