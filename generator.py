#!/usr/bin/env python3

import os
import shutil
import subprocess


class Command(object):
    def __init__(self, executable, *args):
        self.executable = executable
        self.args = args
        self.verbose = True

    def __str__(self):
        return self.executable + ' ' + ' '.join(self.args)

    def execute(self):
        if self.verbose: print('Executing: \"' + str(self) + '\"')
        subprocess.run([self.executable, *self.args], check=True)


class GitCommand(Command):
    def __init__(self, git_command, *args):
        super(GitCommand, self).__init__('git', git_command, *args)


class GitProject(object):
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.commands = [GitCommand('init')]

    def append_command(self, executable, *args):
        self.commands.append(Command(executable, args))

    def append_git_command(self, command, *args):
        self.commands.append(GitCommand(command, *args))

    def append_new_committed_file_command(self, file_root_name):
        self.commands.append(Command('touch', file_root_name+'txt'))
        self.commands.append(GitCommand('add', '.'))
        self.commands.append(GitCommand('commit', '-m', file_root_name))

    def reset(self):
        shutil.rmtree(self.folder_name, ignore_errors=True)

    def initialize(self):
        os.mkdir(self.folder_name)
        os.chdir(self.folder_name)

    def create(self):
        self.reset()
        self.initialize()
        for command in self.commands:
            command.execute()


if __name__ == '__main__':
    gp = GitProject('git-book-v2-chapter-3.1-branches-in-a-nutshell')
    gp.append_new_committed_file_command('98ca9')
    gp.append_new_committed_file_command('34ac2')
    gp.append_new_committed_file_command('f30ab')
    gp.append_git_command('branch', 'testing')
    gp.append_git_command('checkout', 'testing')
    gp.append_new_committed_file_command('87ab2')
    gp.append_git_command('checkout', 'master')
    gp.append_new_committed_file_command('c2b9e')
    gp.create()