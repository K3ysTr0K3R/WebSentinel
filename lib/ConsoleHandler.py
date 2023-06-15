import argparse
from lib.Scanner import *
from lib.Crawler import *
from lib.DNSprayer import *
from lib.ConsoleHandler import *

def default_useragent():
	return "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/19.0 Chrome/102.0.5005.125 Mobile Safari/537.36"

def main():
	parser = argparse.ArgumentParser(description='')
        parser.add_argument('--url', help='Specify the URL of the webpage to crawl.')
        parser.add_argument('--ip', help='Specify the IP address or IP range to scan servers.')
        parser.add_argument('--dns-enum', help='Specify a domain name without the "www" subdomain prefix for enumeration.')
        parser.add_argument('--pdf-spider', help='Crawl all PDF files from a given URL using a spider.')
        parser.add_argument('--useragent', default=default_useragent(), help='Specify a user-agent to be used.')
	args = parser.parse_args()

	if args.url:
		crawler = Crawler(args.useragent)
		crawler.start_crawler(args.url)
	elif args.ip:
		scanner = Scanner()
		scanner.start_scanner(args.ip, args.useragent)
	elif args.dns_enum:
		dns_enumeration = DNSprayer()
		dns_enumeration.start_dns_enumeration(args.dns_enum)

if __name__ == "__main__":
	main()
