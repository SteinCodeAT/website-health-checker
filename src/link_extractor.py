"""This module contains functions to extract links and resources such as scripts and images from a given html webpage."""

from bs4 import BeautifulSoup


def extract_links_in_page(soup: BeautifulSoup):
    links = []

    for link in soup.find_all('a'):
        links.append(link.get('href'))

    return links


def extract_resources_in_page(soup: BeautifulSoup):
    links = []

    for resource in soup.find_all('link'):
        links.append(resource.get('href'))

    scripts = []

    for resource in soup.find_all('script'):
        scripts.append(resource.get('src'))

    images = []
    for resource in soup.find_all('img'):
        images.append(resource.get('src'))

    return scripts, images, links
