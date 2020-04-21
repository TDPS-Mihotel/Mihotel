from colorama import init, Fore, Back, Style


def info(item):
    '''
    Bright green output for normal information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.GREEN + '[Info] ' + item + Style.RESET_ALL)


def debugInfo(item):
    '''
    Bright red output for debug information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.RED + '[Debug] ' + item + Style.RESET_ALL)


def movementInfo(item):
    '''
    Bright yellow output for movement information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.YELLOW + '[Movement] ' + item + Style.RESET_ALL)


def detectedInfo(item):
    '''
    Bright blue output for detected object information
    '''
    item = str(item)
    print(Style.BRIGHT + Fore.BLUE + '[Detected] ' + item + Style.RESET_ALL)


init()  # enable ANSI escape sequences on Windows
