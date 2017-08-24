#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys


# CONSTANTS
DEFAULT_MODULE_DIR = "modules"
SYM_PRINT_INFO = "[*]"
SYM_PRINT_SUCCESS = "[+]"
SYM_PRINT_ERROR = "[-]"


# SEVERALS PRINTS
def _print(symbole, message):
    if not isinstance(symbole, str):
        return TypeError
    if not isinstance(message, str):
        return TypeError

    print "{sym} - {msg}".format(
            sym=symbole, 
            msg=message.capitalize()
    )


def pinfo(message):
    _print(SYM_PRINT_INFO, message)


def psuccess(message):
    _print(SYM_PRINT_SUCCESS, message)


def perror(message):
    _print(SYM_PRINT_ERROR, message)


def listfiles(path):
    if not isinstance(path, str):
        return TypeError
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def listpyfiles(path):
    if not isinstance(path, str):
        return TypeError
    return [os.path.basename(f) for f in glob.glob(os.path.join(path, "*.py"))]

def main_menu():
    pinfo("choose an action pls")
    choice = raw_input(" >> ")
    exec_action(choice)
    return

def exit():
    sys.exit()

actions = {
    'main': main_menu,
    'q': exit,
}

def exec_action(choice):
    ch = choice.lower()
    try:
        actions[ch]()
    except KeyError:
        perror("invalid selection, please try again")
        actions['main']()
    return

if __name__ == "__main__":
    # init
    pinfo("myapp initializing...")
    pinfo("dir of the script being run: %s" % os.path.abspath(__file__))
    cwd = os.getcwd()
    pinfo("current working dir: %s" % cwd)
    # list file in MODULES_DIR
    pinfo("loading modules...")
    lmodules = listpyfiles(cwd + "/" + DEFAULT_MODULE_DIR)
    
    # try to load each module
    for module in lmodules:
        if not module == "__init__.py":
            try:
                cmd_module = __import__(DEFAULT_MODULE_DIR + ".%s"
                        % module[:-3], fromlist=["modules"])
                actions[module[:-3]] = cmd_module.run
                psuccess("  %s" % module[:-3])
            except ImportError:
                perror("    failed to load %s" % module[:-3])

    pinfo("which module do you want to launch ?")
    choice = raw_input(" >> ")
    exec_action(choice) 
