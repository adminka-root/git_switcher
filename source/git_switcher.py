#!/usr/bin/env python3

import os
import sys
import argparse
import json
import re
from subprocess import PIPE, run

class analyze_cli_parameters:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            description='Script to switch git accounts',
            epilog='Adminka-root 2023. https://github.com/adminka-root'
        )

        self.main_group = self.parser.add_argument_group(title='Параметры')

        self.main_group.add_argument(
            '-a', '--add', action='store_true', default=False, required=False,
            help='Add new account'
        )
        self.main_group.add_argument(
            '-d', '--remove', action='store_true', default=False, required=False,
            help='Remove saved accounts'
        )

        self.main_group.add_argument(
            '-s', '--switch', action='store_true', default=False, required=False,
            help='Switch to account'
        )

        self.main_group.add_argument(
            '-l', '--list', action='store_true', default=False, required=False,
            help='Show list of all accounts'
        )

        self.options = self.parser.parse_args(sys.argv[1:])


        options_list = [self.options.add, self.options.remove,  self.options.switch, self.options.list]
        if not (True in options_list):
            # self.get_error('\nPlease specify launch option!')
            self.options.switch = True
        elif len([True for opt in options_list if opt]) > 1:
            self.get_error('\nPlease specify only one option!')

    def get_error(self, message: str):
        self.parser.print_help()
        print(message)
        sys.exit(1)

def create_dir(directory: str, mode='755'):
    mode = int(mode, base=8)
    if os.path.isdir(directory):
        os.chmod(directory, mode)
    else:
        os.makedirs(directory, mode)

def read_json(read_from: str, mode='r'):
    try:
        with open(read_from, mode) as file:
            return json.loads(file.read())
    except:
        raise Exception('Failed to read %s!' % read_from)

def save_json(save_to: str, content, indent=2, mode='w'):
    try:
        with open(save_to, mode) as file:
            return json.dump(content, file, indent=indent)
    except:
        raise Exception('Failed to load %s!' % save_to)

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

def select_from_list(choices: "list of str", type='one'):
    """
    :parameter
        choices: list of str
        type: 'one' or 'many'
    :return list of selected indexs, if type='many'
            or
            int, if type='one'
    """
    output = '\n'.join(
        [str(i) + ': ' + choices[i] for i in range(len(choices))]
    )
    if type == 'many':
        print(output, 'Specify the numbers of the answer separated by a space: ', sep='\n\n')
        while True:
            answer = [int(num) for num in input('Answer: ').split() if len(choices) > int(num)]
            if len(answer) > 0:
                break
        return answer
    else:
        print(output, 'Choose one option number: ', sep='\n\n')
        while True:
            answer = int(input_while_empty('Answer: ').split()[0])
            if len(choices) > answer:
                break
        return answer

def select_yes_or_no(question: str):
    answer = input(question + '\nAnswer[y/N]: ').lower()
    if answer in ['yes', 'y', 'true']:
        return True
    else:
        return False

def return_list_of_all_files_in_dir(directory, regex_exclude=None):
    get_files = []
    for root, dirs, files in os.walk(directory):
        base_root = root
        for file in files:
            if not regex_exclude or not re.match(regex_exclude, file):
                get_files.append(os.path.join(base_root, file))
    return get_files

def input_while_empty(message: str):
    while True:
        answer = input(message)
        if answer.split():
            break
    return answer

class git_switcher:
    def __init__(self, config_file: str, server_name: str):
        self._ssh_dir = os.path.expanduser('~/.ssh/')
        self._config_file = config_file
        self._config_file_exists = os.path.isfile(self._config_file)
        self._config_data = self.read_config()
        if type(self._config_data) != dict:
            self._config_data = dict()

        self._config_dir = os.path.dirname(self._config_file)
        self._server_name = server_name
        self.create_necessary_folders()

    def create_necessary_folders(self):
        create_dir(self._ssh_dir, mode='700')
        create_dir(self._config_dir, mode='700')

    def read_config(self):
        if self._config_file_exists:
            return read_json(self._config_file)
        else:
            return None

    def add_account(self):
        new_account = self.add_account_dialog()
        if self._config_file_exists:
            self._config_data.update(new_account)
        else:
            self._config_data = new_account
        save_json(self._config_file, self._config_data)
        print('\nSuccess!')

    def add_account_dialog(self):
        """
        :return dict
        """
        user = input_while_empty('Enter your git user name: ')
        email = input_while_empty('Enter your git user mail: ')

        need_generated_ssh = select_yes_or_no('Do you want to generate a pair of ssh keys (rsa 2048)?')
        if need_generated_ssh:
            key_name = input_while_empty('Enter key name: ')
            generate_exec = run(
                [
                    'ssh-keygen', '-t', 'rsa', '-b', '2048', '-C', email,
                    '-f', os.path.join(self._ssh_dir, key_name)
                ],
                stdout=PIPE, stderr=PIPE,
                universal_newlines=True
            )
            if generate_exec.returncode == 1:
                raise Exception(generate_exec.stderr)
            else:
                key_file = os.path.join(
                    self._ssh_dir,
                    key_name
                )

        elif select_yes_or_no('Do you want to select from existing keys?'):
            files_in_ssh_dir = return_list_of_all_files_in_dir(
                directory=self._ssh_dir,
                regex_exclude='.*\.pub|known_hosts.*|authorized_keys|config|.*\.json'
            )
            index_of_selected_file = select_from_list(files_in_ssh_dir, type='one')
            key_file = files_in_ssh_dir[index_of_selected_file]
        else:
            key_file = ''

        return {
            user: {
                'email': email,
                'key_file': key_file
            }
        }

    def remove_accounts(self):
        account_for_remove = self.remove_account_dialog()
        for account in account_for_remove:
            del self._config_data[account]
        save_json(self._config_file, self._config_data)
        print('\n', ', '.join(account_for_remove), 'account(s) have been removed!')

    def remove_account_dialog(self):
        if self._config_data:
            print('Select accounts to remove: ')
            usernames = [user for user in self._config_data]
            selected_keys = [usernames[num] for num in select_from_list(usernames, type='many')]
            return selected_keys
        else:
            print('You do not have saved accounts!')
            sys.exit(0)

    def show_all_accounts(self):
        if self._config_data:
            print(json.dumps(self._config_data, sort_keys=True, indent=4))
        else:
            print('You do not have saved accounts!')
            if select_yes_or_no('Do you want to add a new account?'):
                self.add_account()

    def switch_to_account(self):
        username = self.switch_account_dialog()
        email = self._config_data[username]['email']
        private_key = self._config_data[username]['key_file']

        git_commands = [
            # 'git config --global --unset user.name',
            # 'git config --global --unset user.email',
            'git config --global user.name ' + username,
            'git config --global user.email ' + email
        ]
        for git_command in git_commands:
            result = run(
                git_command.split(' '),
                stdout=PIPE, stderr=PIPE,
                universal_newlines=True
            )
            if result.returncode == 1:
                print('\n', git_command)
                print(result.stderr, '\n')

        if private_key:
            result = run(
                ['ssh-add', private_key],
                stdout=PIPE, stderr=PIPE,
                universal_newlines=True
            )
            if result.returncode == 1:
                print('\nssh-add err!')
                print(result.stderr, '\n')

        identity_config = os.path.join(self._ssh_dir, 'config')
        record_block = '\n'.join([
            'Host github.com',
            'IdentityFile ' + private_key if private_key else ''
        ]) + '\n\n'
        success_record_in_config = self.parse_and_edit_config_in_ssh_dir(
            identity_config, record_block
        )
        if success_record_in_config != 0:
            save_file(identity_config, record_block, save_mode='w')
        print('Success switch to', username)

    def parse_and_edit_config_in_ssh_dir(self, identity_config, record_block):
        """
        :return 0 if success else 1
        """
        if os.path.isfile(identity_config):
            identity_config_data = read_file(identity_config)
            search_result = re.finditer('( )*Host.*\n', identity_config_data)  # split by [Host1*, Host2*]...
            start, stop = None, None
            for match in search_result:  # get positions for self._server_name block
                if start is not None:
                    stop = match.start()
                    break
                if re.match('( )*Host\s*' + self._server_name + '( )*\n', match.group()):
                    start = match.start()

            if start is not None:
                if stop is None:
                    identity_config_data = re.sub(
                        identity_config_data[start:],
                        record_block, identity_config_data
                    )
                else:
                    identity_config_data = re.sub(
                        identity_config_data[start:stop],
                        record_block, identity_config_data
                    )
                save_file(identity_config, identity_config_data, save_mode='w')
                return 0
            else:  # not find str 'Host self._server_name'
                identity_config_data = record_block + identity_config_data
                save_file(identity_config, identity_config_data, save_mode='w')
                return 0
        return 1

    def switch_account_dialog(self):
        if self._config_data:
            usernames = [user for user in self._config_data]
            if len(usernames) > 1:
                print('Select account to switch: ')
                selected_account = usernames[select_from_list(choices=usernames, type='one')]
                return selected_account
            else:
                return usernames[0]
        else:
            print('You do not have saved accounts!')
            if select_yes_or_no('Do you want to add a new account?'):
                self.add_account()
            sys.exit(0)


if __name__ == "__main__":
    cli_parameters = analyze_cli_parameters()

    switcher = git_switcher(
        config_file=os.path.join(
            os.path.expanduser('~/.ssh/git_switcher'),
            'accounts.json'
        ),
        server_name='github.com'
    )

    if cli_parameters.options.add:
        switcher.add_account()
    elif cli_parameters.options.remove:
        switcher.remove_accounts()
    elif cli_parameters.options.switch:
        switcher.switch_to_account()
    elif cli_parameters.options.list:
        switcher.show_all_accounts()
