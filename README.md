## 简介
Python实现的某网站小说爬取，并输出成html文件。

## 输出结果
<img width="70%" src="https://github.com/GoOnToDeth/SpiderForFiction/blob/master/images/result.png" />

## 技术细节
* SpiderMain.py 入口类，其中DownloaderHtml用于实现线程调度；
* SpiderBooks.py 获取目标页中所有的小说的url和名称；
* BookCatalog.py 获取所有小说的第一章(节)的url和章(节)名称；
* ArticleDetails.py 获取所有章(节)的标题、内容和url，并输出为html文件

**注意**

html节点的获取使用的是BeautifulSoup，需要安装bs4的库；


