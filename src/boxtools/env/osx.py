#!/usr/bin/env python3

import os
import subprocess


def fix_ip():
    os.system('sudo rm /Library/Preferences/SystemConfiguration/NetworkInterfaces.plist && sudo killall -9 configd')
    print(' - VM ip fixed')


def add_symlink(source_path, target_path):
    os.system('ln -s ' + source_path + ' ' + target_path)


def delete_symlink(target_path):
    os.system('rm ' + target_path)


def copy_to_clipboard(data):
    subprocess.run("pbcopy", universal_newlines=True, input=data)
