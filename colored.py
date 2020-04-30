import os
import platform

from colorama import Back, Fore, Style, init


def info(item):
    '''
    Bright green output for normal information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.GREEN + '[Info] ' + item + Style.RESET_ALL)


def logoInfo():
    '''
    Bright green logo output
    '''
    print(Style.BRIGHT + Fore.GREEN + '''
     /██      /██ /██ /██                   /██               /██
    | ███    /███|__/| ██                  | ██              | ██
    | ████  /████ /██| ███████   /██████  /██████    /██████ | ██
    | ██ ██/██ ██| ██| ██__  ██ /██__  ██|_  ██_/   /██__  ██| ██
    | ██  ███| ██| ██| ██  \ ██| ██  \ ██  | ██    | ████████| ██
    | ██\  █ | ██| ██| ██  | ██| ██  | ██  | ██ /██| ██_____/| ██
    | ██ \/  | ██| ██| ██  | ██|  ██████/  |  ████/|  ███████| ██
    |__/     |__/|__/|__/  |__/ \______/    \___/   \_______/|__/
''' + Style.RESET_ALL)


def debugInfo(item):
    '''
    Bright red output for debug information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.RED + '[Debug] ' + item + Style.RESET_ALL)


def commandInfo(item):
    '''
    Bright blue output for movement information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.BLUE + '[Command] ' + item + Style.RESET_ALL)


def detectedInfo(item):
    '''
    Bright yellow output for detected object information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.YELLOW + '[Detected] ' + item + Style.RESET_ALL)


# FIXME: unknown bug... without this output seems stuck
if (platform.system() is 'Windows') and ('WEBOTS_SERVER' in os.environ):
    init()
