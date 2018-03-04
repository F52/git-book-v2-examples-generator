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
        if self.verbose: print(' > ' + str(self))
        out = None if self.verbose else subprocess.PIPE
        # Awful hack because echo command has no effect with subprocess.run, and I don't know why.
        if self.executable == 'echo':
            with open(self.args[-1], 'a') as f:
                f.write(self.args[0].replace('"', '')+'\n\n')
        else:
            subprocess.run([self.executable, *self.args], check=True, shell=False, stdout=out, stderr=out)


class GitCommand(Command):
    def __init__(self, git_command, *args, verbose=False):
        super(GitCommand, self).__init__('git', git_command, *args, verbose=verbose)


class GitProject(object):
    def __init__(self, folder_name, always_proceed=False, verbose=False):
        self.folder_name = folder_name
        self.always_proceed = always_proceed
        self.verbose = verbose
        self.commands = [GitCommand('init', verbose=verbose)]

    def _append_command(self, executable, *args):
        self.commands.append(Command(executable, *args, verbose=self.verbose))

    def _append_echo_command(self, filename, content):
        self._append_command('echo', '\"' + content + '\"', '>>', filename)

    def git(self, command, *args):
        self.commands.append(GitCommand(command, *args, verbose=self.verbose))

    def append_to_readme(self, content):
        self._append_command('touch', 'README.md')
        self._append_echo_command('README.md', content)
        self.git('add', '.')
        self.git('commit', '-m', 'README')

    def create_new_file(self, filename, content=None, message=None):
        self._append_command('touch', filename)
        if content is not None:
            self._append_echo_command(filename, content)
        self.git('add', '.')
        if message is None:
            message = filename
        self.git('commit', '-m', message)

    def append_content_to_file(self, filename, content, message=None):
        self._append_echo_command(filename, content)
        self.git('add', '.')
        if message is None:
            message = filename
        self.git('commit', '-m', message)

    def override_file_content(self, filename, new_content, message=None):
        self._append_command('rm', '-f', filename)
        self._append_command('touch', filename)
        self._append_echo_command(filename, new_content)
        self.git('add', '.')
        if message is None:
            message = filename
        self.git('commit', '-m', message)

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
    gp.create_new_file('98ca9.txt')
    gp.create_new_file('34ac2.txt')
    gp.create_new_file('f30ab.txt')
    gp.git('branch', 'testing')
    gp.git('checkout', 'testing')
    gp.create_new_file('87ab2.txt')
    gp.git('checkout', 'master')
    gp.create_new_file('c2b9e.txt')
    gp.create()

    gp = GitProject('git-book-v2-chapter-3.2-basic-branching-and-merging-1-figure-21', always_proceed=args.always_proceed, verbose=args.verbose)
    gp.append_to_readme('### Git Book v2 Chapter 3.2 : Figure 21')
    gp.append_to_readme('**Purpose** : do the merge and the delete of hotfix branch yourself.')
    gp.append_to_readme('![Figure 21](https://git-scm.com/book/en/v2/images/basic-branching-4.png)')
    gp.create_new_file('index.html', 'line master c0', message='c0')
    gp.append_content_to_file('index.html', 'line master c1', message='c1')
    gp.append_content_to_file('index.html', 'line master c2', message='c2')
    gp.git('branch', 'iss53')
    gp.git('checkout', 'iss53')
    gp.append_content_to_file('index.html', 'line iss53 c3', message='c3')
    gp.git('checkout', 'master')
    gp.git('branch', 'hotfix')
    gp.git('checkout', 'hotfix')
    gp.append_content_to_file('index.html', 'line hotfix c4', message='c4')
    gp.create()

    gp = GitProject('git-book-v2-chapter-3.2-basic-branching-and-merging-2-figure-24-no-conflict', always_proceed=args.always_proceed, verbose=args.verbose)
    gp.append_to_readme('### Git Book v2 Chapter 3.2 : Figure 24')
    gp.append_to_readme('**Purpose** : do the merge and the delete of iss53 branch yourself.')
    gp.append_to_readme('![Figure 24](https://git-scm.com/book/en/v2/images/basic-merging-1.png)')
    gp.create_new_file('index.html', 'line master c0', message='c0')
    gp.append_content_to_file('index.html', 'line master c1', message='c1')
    gp.append_content_to_file('index.html', 'line master c2', message='c2')
    gp.git('branch', 'iss53')
    gp.git('checkout', 'iss53')
    gp.append_content_to_file('index.html', 'line iss53 c3', message='c3')
    gp.git('checkout', 'master')
    gp.append_content_to_file('index.html', 'line master c4', message='c4')
    gp.git('checkout', 'iss53')
    gp.append_content_to_file('index.html', 'line iss53 c5', message='c5')
    gp.create()

    gp = GitProject('git-book-v2-chapter-3.2-basic-branching-and-merging-3-figure-24-with-conflict', always_proceed=args.always_proceed, verbose=args.verbose)
    gp.append_to_readme('### Git Book v2 Chapter 3.2 : Figure 24')
    gp.append_to_readme('**Purpose** : do the merge by resolving the conflict.')
    gp.append_to_readme('![Figure 24](https://git-scm.com/book/en/v2/images/basic-merging-1.png)')
    gp.create_new_file('index.html', 'line master c0', message='c0')
    gp.append_content_to_file('index.html', 'line master c1', message='c1')
    gp.append_content_to_file('index.html', 'line master c2', message='c2')
    gp.git('branch', 'iss53')
    gp.git('checkout', 'iss53')
    gp.append_content_to_file('index.html', 'line iss53 c3', message='c3')
    gp.git('checkout', 'master')
    gp.append_content_to_file('index.html', 'line master c4', message='c4')
    gp.git('checkout', 'iss53')
    gp.override_file_content('index.html', 'line master c0\n\nline master c1\n\nline master c2\n\nline master \nc4\nhere is a conflicting line...', message='c5')
    gp.create()
