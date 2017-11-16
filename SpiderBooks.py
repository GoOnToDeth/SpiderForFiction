from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.parse


# 全部小说目录类
class BooksList(object):
    def __init__(self):
        self.book_url_list = []
        self.book_name_list = []
        self.count = 1

    def request_book_list(self, start_url):
        try:
            html = self._get_html(start_url)
            self._parser_html(html, start_url)
        except Exception as e:
            print(e)

    def _get_html(self, url):
        response = urlopen(url, data=None, timeout=8)
        if response.getcode() != 200:
            return None
        else:
            html = response.read().decode('utf-8')
            return html

    def _parser_html(self, html, cur_page_url):
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        title_nodes = soup.find("div", class_="self") \
            .find_all("span")
        for node in title_nodes:
            book_url_list = re.findall(r'.+href="(.+?)"', str(node))
            book_name_list = re.findall(r'.+">(.+?)</a>', str(node))
            if len(book_url_list) == 1 and len(book_name_list) == 1:
                book_full_url = urllib.parse.urljoin(cur_page_url, book_url_list[0])
                if book_full_url not in self.book_url_list:
                    self.book_url_list.append(book_full_url)
                    self.book_name_list.append(book_name_list[0])
                    print("%d  %s" % (self.count, book_name_list[0]))
                    self.count += 1

    def get_url_list(self):
        return self.book_url_list
