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
  with open(file_path, 'r+') as file:
    if content not in file.read():
      file.write('\n' + content + '\n')


if __name__ == "__main__":
  script_dir = os.path.abspath(
    os.path.dirname(sys.argv[0]))  # '~/.local/share/git_switcher'
  default_shell = os.path.basename(os.getenv('SHELL', ''))

  rc_file_d = dict(
    bash='~/.bashrc', sh='~/.bashrc',
    zsh='~/.zshrc',
    csh='~/.cshrc', tcsh='~/.cshrc',
  )

  if default_shell not in rc_file_d.keys():
    print(f"Unsupported shell: {default_shell}")
    sys.exit(1)

  if default_shell in ['csh', 'tcsh']:
    need_add = f"""if ( -d '{script_dir}' ) then
    alias git_switcher '{script_dir}/source/git_switcher.py'
    alias git_switcher_uninstall '{script_dir}/uninstall.py'
endif
"""
  else:  # bash/sh/zsh
    need_add = f"""if [ -d '{script_dir}' ]; then
    alias git_switcher='{script_dir}/source/git_switcher.py'
    alias git_switcher_uninstall='{script_dir}/uninstall.py'
fi
"""

  rc_file = rc_file_d[default_shell]
  rc_file_path = os.path.expanduser(rc_file)
  backup_file(rc_file_path)
  backup_file(os.path.expanduser('~/.ssh/config'))

  add_to_rc_file(rc_file_path, need_add)

  print(f"Installation complete. Aliases added to {rc_file}")
