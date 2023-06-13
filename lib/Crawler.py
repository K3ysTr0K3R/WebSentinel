import requests
import re
import html2text
import xml.etree.ElementTree as ET

from lib.ConsoleHandler import *

class Crawler:
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.urls = []
        self.msg = ConsoleHandler()

    def handle_sitemap(self, url, sitemap_response):
        self.msg.success(f"Found sitemap.xml: {url}/sitemap.xml")
        root = ET.fromstring(sitemap_response.content)
        all_urls = []
        for url in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            loc_element = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            if loc_element is not None:
                self.urls.append(loc_element.text)
            for sitemap_urls in all_urls:
                print(sitemap_urls)
            else:
                self.msg.error(f"No sitemap.xml file was found on {url}: {sitemap_response.status_code}")

        self.msg.info("Now crawling webpage for hidden URLs...")

        send_get_page_crawl = requests.get(url, timeout=3, headers={'User-Agent': self.user_agent})
        response = send_get_page_crawl.text
        html_format = html2text.html2text(response)
        regex = re.findall(r'(https?://\S+)', html_format)
        for self.urls in regex:
            stripped_url = re.sub(r'\)', '', self.urls)
            try:
                send_get_page_crawl = requests.get(url, timeout=3, headers={'User-Agent': user_agent})
                status_code = send_get_stripped.status_code

                self.msg.success(f"{stripped_url} - [{status_code}]")
            except requests.exceptions.ConnectionError:
                self.msg.error(f"Connection error occurred for URL: {stripped_url}")
            except Exception:
                pass

    def start_crawler(self, url):
        user_agent = self.user_agent
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
                    self.msg.success(f"Found Login - {found}")
            except requests.exceptions.ConnectionError as e:
                self.msg.error(f"Connection error occurred for URL: {found} -> {e}")
            except Exception:
                pass

        print("")
        self.msg.info(f"Total login pages found: {result_count}")
        print("")
        self.msg.info("Crawling for sitemap URLs...")
        print("")
        sitemap_url = url + "/" + "sitemap_index.xml"
        sitemap_response = requests.get(sitemap_url)
        if sitemap_response.status_code == 200:
            self.handle_sitemap()