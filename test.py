#!/bin/python3

import argparse
import threading
import requests
import html2text
import xml.etree.ElementTree as ET
import re
from netaddr import IPNetwork

def default_useragent():
	return "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-A125F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/19.0 Chrome/102.0.5005.125 Mobile Safari/537.36"

def scan_server(ip, user_agent, count_results):
	try:
		headers = {'User-Agent': user_agent}
		check_http = requests.get("http://" + str(ip), headers=headers, timeout=3)
		response_code_http = check_http.status_code
		server_name_http = check_http.headers.get('Server')
		if check_http.url.startswith('http'):
			print(f"http://{ip} [{server_name_http}] [{response_code_http}]")
			count_results[0] += 1

		check_https = requests.get("https://" + str(ip), headers=headers, timeout=3)
		response_code_https = check_https.status_code
		server_name_https = check_https.headers.get('Server')
		if check_https.url.startswith('https://'):
			print(f"https://{ip} [{server_name_https}] [{response_code_https}]")
			count_results[0] += 1
	except requests.exceptions.RequestException:
		pass

def scan_servers(ip_network, user_agent):
	count_results = [0]
	threads = []
	for ip in ip_network:
		t = threading.Thread(target=scan_server, args=(ip, user_agent, count_results))
		t.start()
		threads.append(t)

	for t in threads:
		t.join()

	return count_results[0]

def crawl_website(url, useragent):
	user_agent = default_useragent()
	logins = {}
	result_count = 0
	admin_panel_directories = [
		'admin',
		'login',
		'dashboard',
		'admin_panel',
		'admin_area',
		'wp-admin',
		'admin-login',
		'cms',
		'cpanel',
		'phpmyadmin',
		'admin.php',
		'login.php',
		'webmail',
		'wp-login.php'
	]

	for directory in admin_panel_directories:
		found = ''
		try:
			crawl_login_get = requests.get(f"{url}/{directory}", timeout=3, headers={'User-Agent': user_agent})
			if crawl_login_get.status_code == 200:
				result_count += 1
				logins[directory] = {
					'username': 'admin',
					'password': 'password',
				}
				found = url + "/" + directory
				print(f"[+] - Found Login - {found}")
		except requests.exceptions.ConnectionError:
			print(f"[!] Connection error occurred for URL: {found}")
			print(f"{e}")
		except Exception:
			pass

	print("")
	print(f"[!] Total login pages found: {result_count}")
	print("")
	print("(i) Crawling for sitemap URLs...")
	print("")
	sitemap_url = url + "/" + "sitemap_index.xml"
	sitemap_response = requests.get(sitemap_url)
	if sitemap_response.status_code == 200:
		print(f"[+] Found sitemap.xml: {url}/sitemap.xml")
		root = ET.fromstring(sitemap_response.content)
		all_urls = []
		for url in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
			loc_element = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
			if loc_element is not None:
				urls.append(loc_element.text)
			for sitemap_urls in all_urls:
				print(sitemap_urls)
			else:
				print(f"[~] No sitemap.xml file was found on {url}: {sitemap_response.status_code}")
	print("")
	print("(i) Now crawling webpage for hidden URLs...")
	print("")
	send_get_page_crawl = requests.get(url, timeout=3, headers={'User-Agent': user_agent})
	response = send_get_page_crawl.text
	html_format = html2text.html2text(response)
	regex = re.findall(r'(https?://\S+)', html_format)
	for urls in regex:
		stripped_url = re.sub(r'\)', '', urls)
		try:
			send_get_page_crawl = requests.get(url, timeout=3, headers={'User-Agent': user_agent})
			status_code = send_get_stripped.status_code
			print(f"[+] - {stripped_url} - [{status_code}]")
		except requests.exceptions.ConnectionError:
			print(f"[!] Connection error occurred for URL: {stripped_url}")
		except Exception:
			pass

def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--url', help='URL to crawl webpage.')
	parser.add_argument('--ip', help='IP address or IP range to scan servers.')
	parser.add_argument('--useragent', default=default_useragent(), help='Add a user-agent.')
	args = parser.parse_args()

	if args.url:
		crawl_website(args.url, args.useragent)
	elif args.ip:
		ip_network = IPNetwork(args.ip)
		count_results = scan_servers(ip_network, args.useragent)
		print("")
		print(f"[+] Found {count_results} results.")

if __name__ == "__main__":
	main()
