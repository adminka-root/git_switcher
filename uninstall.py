#!/usr/bin/env python3

import os
import re
import shutil
import sys


def select_yes_or_no(question: str):
  answer = input(question + '\nAnswer[y/N]: ').lower()
  if answer in ['yes', 'y', 'true']:
    return True
  else:
    return False


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

  # if [ -d '/home/adminka/.local/share/git_switcher' ]; then
  #     alias git_switcher='/home/adminka/.local/share/git_switcher/source/git_switcher.py'
  #     alias git_switcher_uninstall='/home/adminka/.local/share/git_switcher/uninstall.py'
  # fi
  #                       --- OR ---
  # if [ -d '/home/adminka/.local/share/git_switcher' ]; then alias git_switcher='/home/adminka/.local/share/git_switcher/source/git_switcher.py'; alias git_switcher_uninstall='/home/adminka/.local/share/git_switcher/uninstall.py'; fi

  # Easter egg for remigenet:
  #   The .*? construct is a "lazy" operator and can capture text up to
  #   the next pattern match. If your file contains multiple blocks
  #   starting with if [ -d '...' ], the regular expression may
  #   "expand" and capture more than necessary.
  sh_pattern = re.compile(
    r"if \[ -d '([^']*git_switcher[^']*)' \]; then\s*alias git_switcher='[^']*/source/git_switcher.py';?\s*alias git_switcher_uninstall='[^']*/uninstall.py';?\s*fi",
    re.DOTALL
  )
  csh_pattern = re.compile(
    r"if \( -d '([^']*git_switcher[^']*)' \) then\s*alias git_switcher='[^']*/source/git_switcher.py'\s*alias git_switcher_uninstall='[^']*/uninstall.py'\s*endif",
    re.DOTALL
  )

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
        break

  if script_dir:
    if select_yes_or_no(f"The directory {script_dir} will be DELETED. Do you want to continue?"):
      if write_file(rc_path, new_content):
        print(f"Removed git_switcher aliases from {rc_path}")
      try:
        shutil.rmtree(script_dir)
        print("Success!\nUninstallation process complete.")
        print("Please restart your terminal or source your "
              "RC file to apply changes.")
      except Exception as e:
        print(f"[Failed]: {str(e)}")
        sys.exit(1)
    else:
      print("Aborted!")
  else:
    print("Could not find git_switcher installation in RC file.")
    sys.exit(1)


if __name__ == "__main__":
  main()
