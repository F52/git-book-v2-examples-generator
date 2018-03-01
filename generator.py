#!/usr/bin/env python3

import os
import sys
import copy
import shutil
import argparse
import subprocess


class Command(object):
    def __init__(self, executable, *args, verbose=False):
        self.executable = executable
        self.args = args
        self.verbose = verbose

    def __str__(self):
        return self.executable + ' ' + ' '.join(self.args)

    def execute(self):
        if self.verbose: print(' - Executing: \"' + str(self) + '\"')
        out = None if self.verbose else subprocess.PIPE
        subprocess.run([self.executable, *self.args], check=True, stdout=out, stderr=out)


class GitCommand(Command):
    def __init__(self, git_command, *args, verbose=False):
        super(GitCommand, self).__init__('git', git_command, *args, verbose=verbose)


class GitProject(object):
    def __init__(self, folder_name, always_proceed=False, verbose=False):
        self.folder_name = folder_name
        self.always_proceed = always_proceed
        self.verbose = verbose
        self.commands = [GitCommand('init')]

    def append_command(self, executable, *args):
        self.commands.append(Command(executable, args, verbose=self.verbose))

    def append_git_command(self, command, *args):
        self.commands.append(GitCommand(command, *args, verbose=self.verbose))

    def append_new_file_command(self, file_root_name):
        self.commands.append(Command('touch', file_root_name+'txt', verbose=self.verbose))
        self.commands.append(GitCommand('add', '.', verbose=self.verbose))
        self.commands.append(GitCommand('commit', '-m', file_root_name, verbose=self.verbose))

    def reset(self):
        if not self.always_proceed:
            answer = input(' ** WARNING : I am about to erase folder : {0}. Proceed ? [yN]'.format(self.folder_name))
        else:
            answer = 'y'
        if answer == 'y':
            shutil.rmtree(self.folder_name, ignore_errors=True)
        else:
            print(' Ok, fine. Not touching anything.')
        return (answer == 'y')

    def initialize(self):
        os.mkdir(self.folder_name)
        os.chdir(self.folder_name)

    def create(self):
        if self.reset():
            current_dir = os.getcwd()
            self.initialize()
            for command in self.commands:
                command.execute()
            os.chdir(current_dir)

    def duplicate(self, new_folder_name):
        new_self = copy.deepcopy(self)
        new_self.folder_name = new_folder_name
        return new_self


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="display the commands being executed", action="store_true")
    parser.add_argument("-p", "--always_proceed", help="display the commands being executed", action="store_true")
    args = parser.parse_args()

    gp = GitProject('git-book-v2-chapter-3.1-branches-in-a-nutshell', always_proceed=args.always_proceed, verbose=args.verbose)
    gp.append_new_file_command('98ca9')
    gp.append_new_file_command('34ac2')
    gp.append_new_file_command('f30ab')
    gp.append_git_command('branch', 'testing')
    gp.append_git_command('checkout', 'testing')
    gp.append_new_file_command('87ab2')
    gp.append_git_command('checkout', 'master')
    gp.append_new_file_command('c2b9e')
    gp.create()

    gp = GitProject('git-book-v2-chapter-3.2-basic-branching-and-merging-1-hotfix', always_proceed=args.always_proceed, verbose=args.verbose)
    gp.append_new_file_command('c0')
    gp.append_new_file_command('c1')
    gp.append_new_file_command('c2')
    gp.append_git_command('branch', 'iss53')
    gp.append_git_command('checkout', 'iss53')
    gp.append_new_file_command('c3')
    gp.append_git_command('checkout', 'master')
    gp.append_git_command('branch', 'hotfix')
    gp.append_git_command('checkout', 'hotfix')
    gp.append_new_file_command('c4')
    gp.create()

    gp = GitProject('git-book-v2-chapter-3.2-basic-branching-and-merging-2-no-conflict', always_proceed=args.always_proceed, verbose=args.verbose)
    gp.append_new_file_command('c0')
    gp.append_new_file_command('c1')
    gp.append_new_file_command('c2')
    gp.append_git_command('branch', 'iss53')
    gp.append_git_command('checkout', 'iss53')
    gp.append_new_file_command('c3')
    gp.append_git_command('checkout', 'master')
    gp.append_git_command('branch', 'hotfix')
    gp.append_git_command('checkout', 'hotfix')
    gp.append_new_file_command('c4')
    gp.append_git_command('checkout', 'master')
    gp.append_git_command('merge', 'hotfix')
    gp.append_git_command('branch', '-d', 'hotfix')
    gp.append_git_command('checkout', 'iss53')
    gp.append_new_file_command('c5')
    gp.create()

    gp = gp.duplicate('git-book-v2-chapter-3.2-basic-branching-and-merging-3-with-conflict')
    gp.create()
