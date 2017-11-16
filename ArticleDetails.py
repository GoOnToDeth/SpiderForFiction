from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.parse
import os


class ArticleDetails(object):
    def __init__(self):
        self.urls = []
        self.url_content = {}
        self.url_title = {}
        self.story_path = "D:\\Python\\Spider_Project\\spider_txt\\小说"

    def craw_from_urllist(self, urllist):
        for url in urllist:
            self.craw_from_url(url)

    def craw_from_url(self, start_url):
        self.urls.clear()
        self.url_title.clear()
        self.url_content.clear()

        new_url = start_url
        html = self._get_html(new_url)
        story_name = self._get_story_name(html)
        count = 1
        while True:
            try:
                html = self._get_html(new_url)
                if html is not None:
                    title, content, has_next, next_page_url = self._parser_html(html, new_url)
                    self.url_title[new_url] = title
                    self.url_content[new_url] = content
                    self.urls.append(new_url)
                    print("%d %s  %s" % (count, story_name, title))
                    count += 1
                    if has_next is False:
                        break
                    if next_page_url is not None:
                        new_url = next_page_url
            except Exception as e:
                print("分割线---------")
                print(e)
                break
        self._output_html(story_name)

    def _get_html(self, url):
        response = urlopen(url, data=None, timeout=8)
        if response.getcode() != 200:
            return None
        else:
            html = response.read().decode('utf-8')
            return html

    def _get_story_name(self, html):
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        # <span>捡个王爷好种田</span>
        name_node = soup.find("div", class_="wrap book_reader") \
            .find("h1") \
            .find("span")
        name = name_node.get_text()
        return name

    def _parser_html(self, html, cur_page_url):
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        title = self._get_title(soup)
        content = self._get_content(soup)
        has_next_page, next_url = self._has_next(soup, cur_page_url)
        return title, content, has_next_page, next_url

    def _get_title(self, soup):
        # <div class="tc"><h2>正文第一章  后山诈尸</h2></div>
        title_node = soup.find("div", class_="wrap book_reader") \
            .find("div", class_="tc") \
            .find("h2")
        title = title_node.get_text()
        return title

    def _get_content(self, soup):
        txt_all = ""
        content_lines = soup.find("div", class_="wrap book_reader") \
            .find("div", class_="book_con") \
            .find_all("p")
        for line in content_lines:
            a = re.findall(r'<p>(.+?)<span', str(line))
            if len(a) == 1:
                txt_all += "<br/>" + a[0]
        return txt_all

    def _has_next(self, soup, cur_page_url):
        node = soup.find("div", class_="wrap book_key")
        if node is None:
            return True, None
        content_lines = node.find("div", class_="tc key") \
            .find_all("a", href=re.compile(r'/chapter/.'))
        if len(content_lines) == 0:
            return False, None
        for item in content_lines:
            txt = item.get_text()
            if txt == "下一章":
                next_url = item['href']
                next_full_url = urllib.parse.urljoin(cur_page_url, next_url)
                return True, next_full_url
        return False, None

    def _output_html(self, file_name):
        file_name = "%s.html" % file_name
        if not os.path.exists(self.story_path):
            os.mkdir(self.story_path)
        file_full_path = "%s\\%s" % (self.story_path, file_name)
        if os.path.exists(file_full_path):
            os.remove(file_full_path)

        fout = open(file_full_path, 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        for url in self.urls:
            fout.write("""<p><h3 style="text-align: center">%s</h3></p>""" % self.url_title[url])
            fout.write("""<p><h4 style="text-align: center"><a href="%s">%s</a></h4></p>""" % (url, url))
            fout.write("""<p><span style="line-height:26px;">%s</span></p>""" % self.url_content[url])
        fout.write("</body>")
        fout.write("</html>")
        fout.close()


# if __name__ == "__main__":
#     urls = ["http://huayu.baidu.com/chapter/701780/38837612.html"]
#     obj_spider = ArticleDetails()
#     for url in urls:
#         obj_spider.craw_from_url(url)
