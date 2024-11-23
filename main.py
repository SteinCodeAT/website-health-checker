
import argparse

from src.health_checker import WebsiteHealthChecker

def main():
    parser = argparse.ArgumentParser(description='Check a website health status including broken links and missing resources!')

    parser.add_argument('url', type=str, help='The URL of the website to check')
    args = parser.parse_args()

    if not args.url:
        print('Please provide a URL to check the website health status!')
        return
    
    if args.url:
        url = args.url

        if "http" not in url:
            url = "https://" + url

        health_checker = WebsiteHealthChecker(url)

        health_checker.check_website_health()

if __name__ == '__main__':
    main()
