"""This module holds functions to find and parse sitemap.xml files from a given website and return the found urls."""

import requests

from loguru import logger
from bs4 import BeautifulSoup


def parse_sitemapt_xml(sitemap_xml):
    soup = BeautifulSoup(sitemap_xml, features="xml")

    urls = soup.find_all('loc')

    return [url.text for url in urls]

def get_sitemap_urls(url):
    """ Try to find the sitemap.xml file(s) for the given url and return the urls found in it. 
    :param url: The main url of the website without any slash or sub path at the end e.g. https://www.google.com.
    """

    # try the most common location for sitemap.xml first
    sitemap_url = url + '/sitemap.xml'

    response = requests.get(sitemap_url)

    if response.status_code == 200:
        return parse_sitemapt_xml(response.content)
    
    # if sitemap.xml is not found, try sitemap-index.xml
    # and parse the sitemap urls from there for sub sitemap (sitempa-0.xml, sitemap-1.xml, etc.)
    sitemap_urls = []

    sitemap_index_url = url + '/sitemap-index.xml'

    response = requests.get(sitemap_index_url)
    
    if response.status_code == 200:
        sub_sitemaps_urls = parse_sitemapt_xml(response.content)
    
        for sitemap_url in sub_sitemaps_urls:
            response = requests.get(sitemap_url)

            if response.status_code == 404:
                # This should never happen and indicates more substantial problems with the website
                raise Exception(f"The sub sitemap {sitemap_url} which was fetched from sitemap-index.xml could not be found!")
            
            sitemap_urls.extend(parse_sitemapt_xml(response.content))

    return sitemap_urls
