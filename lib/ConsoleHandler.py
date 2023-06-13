from termcolor import colored

class ConsoleHandler:
    def __init__(self):
        pass

    def error(self, message):
        print(colored('[-] ', 'red') + message)

    def success(self, message):
        print(colored('[+] ', 'green') + message)

    def info(self, message):
        print(colored('[*] ', 'yellow') + message)

