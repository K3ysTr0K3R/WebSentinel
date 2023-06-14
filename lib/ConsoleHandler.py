from termcolor import colored

class ConsoleHandler:
    def __init__(self):
        pass

    def error(self, message):
        print(colored('[-] ', 'red') + message)

    def success(self, message):
        print(colored('[+] ', 'green') + message)

    def info(self, ip_address, server_name, response_code):
        print(colored('[*] ', 'yellow') + colored(ip_address, 'cyan') + f" [{server_name}] [{response_code}]")
