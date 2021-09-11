from get_image import get_urls
from get_abs_url import get_abs_url
from check_url_type import check_url_type
from save_image import save_image


urls = get_urls('https://gihyo.jp/book/list')
try:
    for abs_url in urls:
        abs_url = get_abs_url('https://gihyo.jp/book/list',abs_url)
        if check_url_type(abs_url):
            save_image(abs_url, abs_url)
except Exception as e:
    print("Error")