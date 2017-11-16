from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse


# 当前小说目录类
class BookCatalog(object):
    def request_chapter_info(self, start_url):
        try:
            html = self._get_html(start_url)
            return self._get_first_chapter_info(html, start_url)
        except Exception as e:
            return None

    def _get_html(self, url):
        response = urlopen(url, data=None, timeout=8)
        if response.getcode() != 200:
            return None
        else:
            html = response.read().decode('utf-8')
            return html

    # 获取第一章相关信息
    def _get_first_chapter_info(self, html, cur_url):
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        url_node = soup.find("div", class_="con bordec_notop") \
            .find("span", class_="chapname") \
            .find("a")
        # 第一章 链接
        first_chapter_url = url_node['href']
        # 第一章 标题
        first_chapter_title = url_node.get_text()
        # 第一章全连接
        chapter_full_url = urllib.parse.urljoin(cur_url, first_chapter_url)
        return chapter_full_url, first_chapter_title
