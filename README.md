# 🌐 Website Health Checker

This python script checks a given website for the following health issues:

1. Availability of the main URL
2. Broken external links
3. Broken internal links to pages 
4. Broken internal links to resources such as images, scripts and css
5. Redirected URLs

This script crawls the given website and extracts all links as well as resources and then tries to call those using python requests. Each link is then logged as working, redirected or broken. At the end, an html report is created which gives details on the results.

## Problem

When managing a website it can quickly become difficult to ensure that all links are working and correctly set. Broken links can be caused by something simple like a typo, but it can also happen that the referenced page was moved without adjusting all referencing links.

From a user perspective broken links are frustrating and appear unprofessional. But also SEO is harmed by broken links as the engines can no longer link content together.

Redirected URLs can indicate a problem like for instance if you reference one of your blog pages but forget to add a slash at the end. In this case the user is redirected to the url version with the slash at the end. This might not be a big issue but has to be looked at on a case-by-case basis.

Since links can break at any time by accident or misfortune, it is important to regularely check all set links on a website. This script is intended to simplify this process.

## Getting Started

### Installation

This repository requires python 3.12+.

Clone the repository (or download it). Then, create a new virtual environment and install the dependencies. This repository uses pipenv for that.

```python
pipenv install
```

After that activate the new environment:

```python
pipenv shell
```

### Usage

To start the script, execute main.py and provide the URL of your website:

```python
python main.py <your-url>
```

The script will now look for your sitemap.xml and crawl each page referenced in it and checking all internal and external link it can find.

The final report is saved in the /reports folder in the root of the project. If the folder does not exist, the script will create it for you.

### Additional Configurations

Additional settings can be defined in a config.json file in the root directory.

|key|allowed values|Description|
|:--|:--|:--|
|valid_email_addresses|a list of email adresses as strings|Any mail address found on the website is compared with this list if it has a recipient set.|
|skip_check_urls|a list of urls as strings|URLs defined here are not checked using requests. This is useful for social media account urls which are quite restricting regarding python requests|
|skip_check_url_patterns|a list of url components as strings|If an URL contains this component it is not checked using requests. This is useful for sharing urls for social media which are quite restricting regarding python requests|

## License

The code is available under the MIT license.
