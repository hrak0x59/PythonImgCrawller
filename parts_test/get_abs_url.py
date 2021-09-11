import urllib.parse

def get_abs_url(current_url,url):
    abs_url = urllib.parse.urljoin(current_url,url)
    return abs_url
'''
print(get_abs_url('https://gihyo.jp/book/list','http://gihyo.jp/site/inquiry'))
print(get_abs_url('https://gihyo.jp/book/list','/book/2017/978-4-7741-8751-98'))
print(get_abs_url('https://gihyo.jp/book/list','2017/978-4-7741-8751-98'))
'''