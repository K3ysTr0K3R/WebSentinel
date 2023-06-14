import requests

main_domain = "porn.com"
with open('subdomains-top1mil-20000.txt', 'r') as wordlist:
    for subdomain in wordlist.read().split('\n'):
        subdomain_url = "http://" + subdomain + "." + main_domain
        try:
            subdomain_url_http_https = requests.get(subdomain_url)
            if subdomain_url_http_https.url.startswith('http'):
                response_code = subdomain_url_http_https.status_code
                if response_code == 200:
                    print(subdomain_url)
            #elif
        except requests.exceptions.RequestException:
            pass
