""" This module holds the main health checking class. It is reponsible for checking the health status of a website, 
including broken links and missing resources. It is the main entry point of the application. """

from typing import List

import enum
from dataclasses import dataclass

from pathlib import Path

import json

import time
import random

import requests
from bs4 import BeautifulSoup
from loguru import logger

from src.data_objects import LinkRecord, LinkType
from src.link_extractor import extract_links_in_page, extract_resources_in_page
from src.sitemap import get_sitemap_urls
from src.report import HtmlReportPrinter


class WebsiteHealthChecker:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept-Language": "de-DE,de;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/"
    }

    def __init__(self, main_url):
        self.main_url = main_url

        # Instantiate needed classes
        self.report_printer = HtmlReportPrinter()

        # main record of broken links and missing resources
        self.broken_links: List[LinkRecord] = []
        self.redirected_links : List[LinkRecord] = []

        # used as cache to avoid checking the same link/resource multiple times
        self.working_links: List[LinkRecord] = []

        # Paths
        self.root_path = Path(__file__).parent.parent

        # get base config
        self.config_file_path = self.root_path.joinpath("config.json")

        if not self.config_file_path.exists():
            logger.error("Config file not found! Place a config.json file in the root directory of the project!")

        with open(self.config_file_path, "r") as file:
            self.config = json.load(file)

        self.valid_email_addresses = self.config.get("valid_email_addresses", [])
        self.skip_check_urls = self.config.get("skip_check_urls", [])
        self.skip_check_url_patterns = self.config.get("skip_check_url_patterns", [])

        logger.info(f"Found the following valid email addresses in the config file: {self.valid_email_addresses}")

    def _check_link_health(self, origin_page_url, link, link_type):
            if not link:
                # skip empty links that have no href or src attribute (inline script tags, etc.)
                return

            if link in self.skip_check_urls:
                # skip links that are defined in the config file as valid
                self.working_links.append(LinkRecord(link=link, found_in_page=[origin_page_url], resource_type=link_type, status_code="SKIP-URL"))
                return
            
            for pattern in self.skip_check_url_patterns:
                if pattern in link:
                    # skip links that match a pattern defined in the config file - e.g. social media sharing links.
                    # Social media pages are often highly restrictive and not reachable with requests
                    self.working_links.append(LinkRecord(link=link, found_in_page=[origin_page_url], resource_type=link_type, status_code="SKIP-PATTERN"))
                    return

            if link[0] == "#":
                # add the origin_page_url to id-links
                link = origin_page_url + link

            if link[0] == "/":
                # add the main_url to links relative to the domain
                link = self.main_url + link

            if link[0] != "h" and link[0] != "/" and "mailto" not in link:
                # add the origin_page_url to relative links
                link = origin_page_url + link
            
            # check if the link has already been checked
            for working_link in self.working_links:
                if working_link.link == link:
                    working_link.found_in_page.append(origin_page_url)
                    return
                
            for redirected_link in self.redirected_links:
                if redirected_link.link == link:
                    redirected_link.found_in_page.append(origin_page_url)
                    return
            
            for broken_link in self.broken_links:
                if broken_link.link == link:
                    broken_link.found_in_page.append(origin_page_url)
                    return
                
            logger.info(f"Checking link: {link}")

            if link.startswith("mailto"):
                # Check if email address links are valid
                # remove the mailto: prefix and any query parameters
                mail_address_in_link = link.replace("mailto:", "").split("?")[0]
                logger.info(f"Checking email address: {mail_address_in_link}, {link}")
                if mail_address_in_link and mail_address_in_link not in self.valid_email_addresses:
                    self.broken_links.append(LinkRecord(link=link, found_in_page=[origin_page_url], resource_type=LinkType.EMAIL, status_code=""))
                    return
                
                self.working_links.append(LinkRecord(link=link, found_in_page=[origin_page_url], resource_type=LinkType.EMAIL, status_code=""))
                return
            
            # Standard link - check if it is reachable
            time.sleep(0.5 + 1 * random.randint(0, 1))

            try:
                response = requests.get(link, headers=self.HEADERS)

            except requests.exceptions.RequestException as e:
                logger.error(f"Error while checking link: {link} - {e}")
                self.broken_links.append(LinkRecord(link=link, found_in_page=[origin_page_url], resource_type=link_type, status_code="ERROR"))
                return
                    
            link_record = LinkRecord(link=link, found_in_page=[origin_page_url], resource_type=link_type, status_code=response.status_code)

            if response.status_code not in [200, 400, 403, 999]:
                # a link is defined as not to be broken if it returns 200, 400 or 403 (999 is used by linkedin to block scraping)
                # 403 is used as a workaround, since this is usually caused by calling the page with python requests
                # 404 and 500 codes are considered broken
                self.broken_links.append(link_record)
                return
            
            if response.history:
                # check if the link was redirected
                link_record.status_code = response.history[0].status_code
                self.redirected_links.append(link_record)
                return

            self.working_links.append(link_record)

    def check_website_health(self):
        logger.info(f"Checking reachability of main url: {self.main_url}")

        response = requests.get(self.main_url, headers=self.HEADERS)

        main_url_record = LinkRecord(link=self.main_url, found_in_page=["Main URL"], resource_type=LinkType.LINK, status_code=response.status_code)

        if response.status_code != 200:
            logger.info(f"Main URL could not be reached!")
            return
        
        self.working_links.append(main_url_record)

        sitemap_urls = get_sitemap_urls(self.main_url)

        for index, url in enumerate(sitemap_urls):
            time.sleep(1)

            if index < 4:
                pass
                # continue
                
            if index > 5:
                pass
                # break

            logger.info(f"Checking sitemap-url #{index}: {url}")
            response = requests.get(url, headers=self.HEADERS)

            sitemap_link_record = LinkRecord(link=url, found_in_page=["Sitemap"], resource_type=LinkType.LINK, status_code=response.status_code)

            if response.status_code != 200:
                self.broken_links.append(sitemap_link_record)
                continue

            self.working_links.append(sitemap_link_record)

            soup = BeautifulSoup(response.content, features="html.parser")

            links = extract_links_in_page(soup)
            scripts, images, other_links = extract_resources_in_page(soup)

            for link in links:
                self._check_link_health(url, link, LinkType.LINK)

            for script in scripts:
                self._check_link_health(url, script, LinkType.SCRIPT)

            for image in images:
                self._check_link_health(url, image, LinkType.IMAGE)

            for other_link in other_links:
                self._check_link_health(url, other_link, LinkType.OTHER_LINK)
            
        self.report_printer.print_report(
            broken_links=self.broken_links,
            working_links=self.working_links,
            redirected_links=self.redirected_links
        )
        return
    