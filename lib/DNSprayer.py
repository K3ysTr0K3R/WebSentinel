import requests

main_domain = "love.com"
with open('subdomains-top1mil-20000.txt', 'r') as wordlist:
    for subdomain in wordlist.read().split('\n'):
        url = "http://" + subdomain + "." + main_domain
        try:
            response = requests.get(url, timeout=5)
            if response.url.startswith('https'):
                print(response.url)
            else:
                print(response.url)
        except requests.exceptions.RequestException:
            pass
