import argparse
from lib.Scanner import *
from lib.Crawler import *
from lib.DNSprayer import *
from lib.ConsoleHandler import *

def default_useragent():
	return "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/19.0 Chrome/102.0.5005.125 Mobile Safari/537.36"

def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--url', help='URL to crawl webpage.')
	parser.add_argument('--ip', help='IP address or IP range to scan servers.')
	parser.add_argument('--dns-enum', help='Add a domain name without the www sub at the beginning.')
	parser.add_argument('--pdf-spider', help='Spider crawl all PDF files from a given URL')
	parser.add_argument('--useragent', default=default_useragent(), help='Add a user-agent.')
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

