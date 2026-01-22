#!/usr/bin/env python3
import subprocess


def has_poetry():
    try:
        subprocess.run(['poetry', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False