import requests

main_domain = "love.com"
with open('subdomains-top1mil-20000.txt', 'r') as wordlist:
    for subdomain in wordlist.read().split('\n'):
        subdomain_url = "http://" + subdomain + "." + main_domain
        try:
            subdomain_url_response = requests.get(subdomain_url, timeout=5)
            if subdomain_url_response.url.startswith('https'):
                print(subdomain_url_response.url)
            else:
                print(subdomain_url_response.url)
        except requests.exceptions.RequestException:
            pass
