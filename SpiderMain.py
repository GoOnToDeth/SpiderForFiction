from ArticleDetails import ArticleDetails
from BookCatalog import BookCatalog
from SpiderBooks import BooksList
from threading import Thread
import math


class DownloaderHtml(Thread):
    def __init__(self, threadname, task_list):
        Thread.__init__(self, name=threadname)
        self.task_list = task_list

    def run(self):
        objDetails = ArticleDetails()
        objDetails.craw_from_urllist(self.task_list)


if __name__ == "__main__":
    page_count = 1
    # 获取全部小说链接
    objBookList = BooksList()
    for i in range(1, page_count + 1):
        start_url = "http://huayu.baidu.com/history/recommend/7/32/%s.html" % i
        objBookList.request_book_list(start_url)
    bookUrlList = objBookList.get_url_list()
    # 获取全部小说的第一章信息
    objCatalog = BookCatalog()
    first_chapter_url_list = []
    count = 1
    for book_url in bookUrlList:
        first_chapter_url, first_chapter_title = objCatalog.request_chapter_info(book_url)
        if first_chapter_url is not None:
            first_chapter_url_list.append(first_chapter_url)
            print("%d  %s  %s" % (count, first_chapter_url, first_chapter_title))
            count += 1
    # 开启线程下载
    max_thread_count = 5
    step = math.ceil(len(first_chapter_url_list) / max_thread_count)
    cur_pos = 0
    selcted_task_list = []
    len_total_url = len(first_chapter_url_list)
    while cur_pos < len_total_url:
        end_pos = cur_pos + step
        if end_pos > len_total_url:
            end_pos = len_total_url
        task_list = first_chapter_url_list[cur_pos: end_pos]
        # 开始下载
        threadDownloader = DownloaderHtml(str(cur_pos), task_list)
        threadDownloader.start()
        cur_pos = end_pos
    print("%d个线程，启动完毕" % max_thread_count)
