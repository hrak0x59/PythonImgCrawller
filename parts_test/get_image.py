import requests
import re

def get_urls(url):
    response = requests.get(url)
    html = response.text

    urls = re.findall('<img src="?\'?([^"\'>]*)',html)
    return urls

print(get_urls('https://gihyo.jp/book/list'))