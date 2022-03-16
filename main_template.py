from copy import deepcopy
from scraping_tool_selenium import DynamicWebScraper, By
# from requests_scraping_tool import scrape_one_page, scrape_all_pages
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit, urlencode


def parser(html_doc):
    souped = BeautifulSoup(html_doc, "html.parser")
    elements = souped.select('div.quote')
    quotes = list()
    for element in elements:
        quotes.append(element.get_text(strip=True, separator=";"))
    return quotes


def page_urls(old_url, num_pages):
    split_url = urlsplit(old_url)
    new_scheme = split_url.scheme
    new_netloc = split_url.netloc
    new_query = split_url.query
    new_fragment = split_url.fragment
    for i in range(num_pages):
        new_path = f"page/{i+1}"
        yield urlunsplit((new_scheme, new_netloc, new_path, new_query, new_fragment))


url = "https://quotes.toscrape.com/"
chrome = DynamicWebScraper(base_url=url, time_wait=10)
chrome.options.add_argument('--disable-extension')
# chrome.options.add_argument('--headless')
chrome.options.add_argument('--start-maximized')
# chrome.options.add_experimental_option("detach", True)
chrome.options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome.options.page_load_strategy = 'eager'
chrome.launch_driver(options=chrome.options)
chrome.add_page_urls(page_urls=page_urls(url, 10))
chrome.add_parser(fparser=parser)
chrome.scrape_all_pages()
items = deepcopy(chrome.page_items)
chrome.quit()
print("\n")
for i in items:
    print(i)