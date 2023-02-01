# Description

Changing git accounts is a problem (see [here](https://gist.github.com/aprilmintacpineda/f101bf5fd34f1e6664497cf4b9b9345f) and [here](https://gist.github.com/jexchan/2351996)) that requires user attention. This repository integrates a script to easily switch between different accounts.

By default, the script is configured to switch with server_name='github.com'. If you are interested in a different server, you can manually override this behavior in the script itself.

```bash
20:53:11 ▶ ./git_switcher.py -h
usage: ./git_switcher.py [-h] [-a] [-d] [-s] [-l]

Script to switch git accounts

optional arguments:
  -h, --help    show this help message and exit

Параметры:
  -a, --add     Add new account
  -d, --remove  Remove saved accounts
  -s, --switch  Switch to account
  -l, --list    Show list of all accounts

Adminka-root 2023. https://github.com/adminka-root
```

## Usage example

```bash
20:57:40 ▶ git_switcher
You do not have saved accounts!
Do you want to add a new account?
Answer[y/N]: y
Enter your git user name: Superman
Enter your git user mail: thebest@superman.com
Do you want to generate a pair of ssh keys (rsa 2048)?
Answer[y/N]: Y
Enter key name: you_can't_hack_me!                 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 

Success!
21:01:42 ▶ git_switcher
Success switch to Superman
21:01:54 ▶ git_switcher -l
{
    "Superman": {
        "email": "thebest@superman.com",
        "key_file": "/home/superman/.ssh/you_can't_hack_me!"
    }
}
21:02:13 ▶ git_switcher -d
Select accounts to remove: 
0: Superman

Specify the numbers of the answer separated by a space: 
Answer: 0

 Superman account(s) have been removed!
```

## Installation

Make a backup copy of the important system files that the script uses. This is optional, but good practice:

```bash
if [[ -f ~/.ssh/config ]]; then cp ~/.ssh/config ~/.ssh/config.bak; fi
cp ~/.profile ~/.profile.bak
```

Then:

```bash
cd ~/.local/share/
git clone https://github.com/adminka-root/git_switcher.git
cd git_switcher
python3 install.py
source ~/.profile
```

## Uninstalling

```bash
git_switcher_uninstall
```

