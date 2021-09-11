#URLのhtmlの中の英語であるものの意味を全て英和辞典で調べるゴミシステム
#めっちゃ遅くなるよ＾
#サーバーダウン気を付けてね
import webbrowser
import time
import requests
import re
html = requests.get('https://www.seibido.co.jp/np/en/code/9784791945641/')
html = html.text
m = re.findall(r'\w+', html)
english_lists = []
for i in m:
    if i.isalpha() and i.isascii():
            english_lists.append(i)

for i in english_lists:
    webbrowser.open('https://ejje.weblio.jp//content/' + i)
    time.sleep(2)

