import requests
import threading
from lib.ConsoleHandler import *

class Scanner:
    def __init__(self):
        self.msg = ConsoleHandler()

    def dns_enum(self, main_domain):
        subdomains = []
        with open('subdomains-top1mil-20000.txt', 'r') as wordlist:
            subdomains = wordlist.read().split('\n')
        batch_size = 100
        num_threads = len(subdomains) // batch_size + 1

        def process_batch(subdomains_batch):
            session = requests.Session()
            for subdomain in subdomains_batch:
                subdomain_url = "http://" + subdomain + "." + main_domain
                try:
                    subdomain_url_response = session.get(subdomain_url, timeout=5)
                    if subdomain_url_response.url.startswith('https'):
                        self.msg.more_info(subdomain_url_response.url)
                    else:
                        self.msg.more_info(subdomain_url_response.url)
                except requests.exceptions.RequestException:
                    pass

        threads = []
        for i in range(num_threads):
            start_index = i * batch_size
            end_index = (i + 1) * batch_size
            subdomains_batch = subdomains[start_index:end_index]
            thread = threading.Thread(target=process_batch, args=(subdomains_batch,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

scanner = Scanner()
main_domain = 'love.com'
threading.Thread(target=scanner.dns_enum, args=(main_domain,)).start()
