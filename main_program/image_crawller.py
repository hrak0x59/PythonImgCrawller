import re
import os
import urllib
import requests

class ImageCrawller:
    def __init__(self,save_dirpath,start_page,maximum_download):
        self.save_dirpath = save_dirpath
        self.crawl_url_list = [start_page]
        self.stocked_url = set()
        self.maximum_download = maximum_download
        self.download_counter = 0

#あるurlのhtmlに含まれる絶対urlをリストで返すメソッド
    def get_abs_urls(self,url):
        try:
            #URLから文字列のhtmlを取得
            response = requests.get(url)
            html = response.text

            #URLからURLを抜き出してリストに格納
            relative_url_list = re.findall('<img src="?\'?([^"\'>]*)',html)
            #相対urlを絶対urlに変換。http/https以外のurlは除外
            abs_url_list = []
            for relative_url in relative_url_list:
                abs_url = urllib.parse.urljoin(url,relative_url)
                if abs_url.startswith('http://') or abs_url.startswith('https://'):
                    abs_url_list.append(abs_url)
            return abs_url_list
        except Exception as e:
            print('Error1:{}'.format(e))
            return []

#urlをhtmlと画像に振り分けるメソッド
    def get_image_url_list(self,url_list):
        try:
            image_url_list = []
            for url in url_list:
                if url in self.stocked_url: #既に登録されたurlなので無視
                    continue
                
                if '.jpg' or '.png' or '.gif' or '.jpeg' in url:
                    image_url_list.append(url)
                else:
                    self.crawl_url_list.append(url) #画像ファイルではないのでurl取得に使う
                self.stocked_url.add(url) #URLを登録。同じものは再登録しない。重複できないように。
            return image_url_list
        
        except Exception as e :
            print('Error2:{}'.format(e))
            return []
                
#イメージを保存するメソッド
    def save_image(self,image_url_list):
        for image_url in image_url_list:
            try:#決められた回数以上をダウンロードした場合は終了
                if self.download_counter >= self.maximum_download:
                    return 
                #イメージを取得
                response = requests.get(image_url,stream=True)
                image = response.content
                #イメージをファイルに保存
                file_name = image_url.split('/').pop()
                save_path = os.path.join(self.save_dirpath,file_name)
                with open(save_path,'wb') as f:
                    f.write(image)
                
                self.download_counter += 1
                print('saved image:{}/{}'.format(self.download_counter,self.maximum_download))

            except Exception as e :
                print('Error3:{}'.format(e))

#上記を3つを束ねる中心となるメソッド
    def run(self):
        while True:
            #処理1:探索するURLがなければ終了。もしくは規定数以上を集めていても終了
            if len(self.crawl_url_list) == 0:
                break
            if self.download_counter >= self.maximum_download:
                break
            #処理2:次に調べるHTMLのURLを取得
            craw_url = self.crawl_url_list.pop(0)
            #処理3:htmLページから絶対URLを取得
            urls = self.get_abs_urls(craw_url)
            #処理4:絶対urlをhtmLかイメージかに分類する。イメージのリストを返す
            image_url_list = self.get_image_url_list(urls)
            #処理5:リストに格納されたイメージをすべて保存する
            self.save_image(image_url_list)

            print('Finished')

if __name__=='__main__':
    save_dirpath = 'test'
    start_page = 'https://gihyo.jp/book/list'
    maximum_download = 10
    crawller = ImageCrawller(save_dirpath,start_page,maximum_download)
    crawller.run()
