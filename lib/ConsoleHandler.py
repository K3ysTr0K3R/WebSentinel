from termcolor import colored
from datetime import datetime

time_date = datetime.now().strftime("%H:%M:%S")

class ConsoleHandler:
    def __init__(self):
        pass

    def error(self, message):
        print(colored('[-] ', 'red') + message)

    def success(self, message):
        print(colored('[+] ', 'green') + message)

    def info(self, ip_address, server_name, response_code):
        print(colored('[*] ', 'yellow') + colored(ip_address, 'cyan') + f" [{server_name}] [{response_code}]")

    def more_info(self, subdomain_url_response_url):
        print(colored('[' + time_date + '] ', 'cyan') + colored('[INFO]', 'green') + colored(' ['+ subdomain_url_response_url  + ']'))
