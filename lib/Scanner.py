import requests
import threading
from netaddr import IPNetwork

from lib.ConsoleHandler import *

class Scanner:
    def __init__(self):
        self.msg = ConsoleHandler()

    def scan_server(self, ip, user_agent, count_results):
        try:
            headers = {'User-Agent': user_agent}
            check_http = requests.get("http://" + str(ip), headers=headers, timeout=3)
            response_code_http = check_http.status_code
            server_name_http = check_http.headers.get('Server')
            if check_http.url.startswith('http'):
                self.msg.info(f"http://{ip} [{server_name_http}] [{response_code_http}]")
                count_results[0] += 1

            check_https = requests.get("https://" + str(ip), headers=headers, timeout=3)
            response_code_https = check_https.status_code
            server_name_https = check_https.headers.get('Server')
            if check_https.url.startswith('https://'):
                self.msg.info(f"https://{ip} [{server_name_https}] [{response_code_https}]")
                count_results[0] += 1
        except requests.exceptions.RequestException:
            pass

    def scan_servers(self, ip_network, user_agent):
        count_results = [0]
        threads = []
        for ip in ip_network:
            t = threading.Thread(target=self.scan_server, args=(ip, user_agent, count_results))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return count_results[0]
    
    def start_scanner(self, ip, user_agent):
        ip_network = IPNetwork(ip)
        count_results = self.scan_servers(ip_network, user_agent)
        self.msg.success(f"Found {count_results} results")