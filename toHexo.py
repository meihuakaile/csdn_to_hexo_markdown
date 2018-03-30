#!/usr/bin/env python2
# coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import codecs
# https://github.com/aaronsw/html2text
import html2text
import argparse
import sys

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')


# responsible for printing
class PrintLayer(object):
    """docstring for PrintLayer"""

    def __init__(self, arg):
        super(PrintLayer, self).__init__()
        self.arg = arg

    @staticmethod
    def printWorkingPage(page):
        print "Work in Page " + str(page)

    @staticmethod
    def printWorkingArticle(article):
        print "Work in " + str(article)

    @staticmethod
    def printWorkingPhase(phase):
        print "Phase 2: Exporting"

    @staticmethod
    def printArticleCount(count):
        print 'Count of Articles: ' + str(count)

    @staticmethod
    def printOver():
        print 'All the posts has been downloaded. If there is any problem, feel free to file issues in https://github.com/gaocegege/csdn-blog-export/issues'


class Analyzer(object):
    """docstring for Analyzer"""

    def __init__(self):
        super(Analyzer, self).__init__()

    # get the page of the blog by url
    def get(self, url):
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        req = urllib2.Request(url, headers=headers)
        html_doc = urllib2.urlopen(req).read()
        return html_doc

    # get the detail of the article
    def get_content(self, soup):
        return soup.find(id='container').find(id='body').find(id='main').find(class_='main')


class Exporter(Analyzer):
    """docstring for Exporter"""

    def __init__(self):
        super(Exporter, self).__init__()

    # export as markdown
    def export_2_markdown(self, f, detail):
        f.write("---\n")
        # 标题
        title = detail.find(class_='article_title').h1.span.a.getText().strip()
        f.write("title: " + title + "\n")
        # 标签
        link_categories = detail.find(class_="link_categories")
        tags = link_categories.find_all("a") if link_categories is not None else []
        taglist = []
        for tag in tags:
            taglist.append(tag.get_text().strip().encode('utf-8'))
        f.write("tags: " + str(taglist).decode('string_escape') + "\n")
        # 种类,去掉csdn上的数字
        category_r = detail.find(class_="category_r")
        categories = category_r.find_all("span") if category_r is not None else []
        category_list = []
        for category in categories:
            all = category.get_text().strip().encode('utf-8')
            num = category.find('em').get_text().strip().encode('utf-8')
            category_list.append(all[: -len(num)])
        f.write("categories: " + str(category_list).decode('string_escape') + "\n")
        # 如果主题配置了版本，没有就把这行注释掉
        f.write("copyright: true\n")
        f.write("---\n")
        content = detail.find(class_='article_content')
        f.write(html2text.html2text(content.prettify()))

    # export
    def export(self, link):
        html_doc = self.get(link)
        soup = BeautifulSoup(html_doc, 'lxml')
        detail = self.get_content(soup).find(id='article_details')
        title = detail.find(class_='article_title').h1.span.a.getText().replace('/', ' ').strip()
        import os
        filename = os.path.join("./markdown/", title)
        # 名字中可能包含特殊字符出错，特别是在windows下。101行的代码已经对/进行了处理。
        # 如果问题很多懒得解决，把154行的注释放开做稍微修改，用文章url里的数字作为文章名字
        try:
            f = codecs.open(filename + '.md', 'w', encoding='utf-8')
            self.export_2_markdown(f, detail)
            f.close()
        except IOError as ioerror:
            print '文件名字中可能包含特殊字符出错，特别是在windows下。101行的代码已经对/进行了处理。' \
                  '如果问题很多懒得解决，把154行的注释放开做稍微修改，用文章url里的数字作为文章名字 \n', ioerror
        return


class Parser(Analyzer):
    """docstring for parser"""

    def __init__(self):
        super(Parser, self).__init__()
        self.article_list = []
        self.page = -1

    # get the articles' link
    def get_one_page_article_url(self, html_doc):
        soup = BeautifulSoup(html_doc)
        res = soup.find('div', class_='list_item_new').find_all('div', class_='list_item clearfix article_item')
        for ele in res:
            self.article_list.append(ele.find(class_='article_title').h1.span.a['href'])

    # get the page of the blog
    def getPageNum(self, html_doc):
        soup = BeautifulSoup(html_doc)
        ul = soup.find("ul", class_="pagination justify-content-center")
        pages = ul.find_all('a', class_="page-link")
        self.page = int(pages[-2].get_text())
        return self.page

    # get all the link
    def getAllArticleUrl(self, url):
        self.getPageNum(self.get(url))
        for i in range(1, self.page + 1):
            PrintLayer.printWorkingPage(i)
            self.get_one_page_article_url(self.get(url + '/article/list/' + str(i)))

    # export the article
    def export(self):
        PrintLayer.printArticleCount(len(self.article_list))
        for link in self.article_list:
            PrintLayer.printWorkingArticle(link)
            exporter = Exporter()
            # exporter.run(link， link.split('/')[6])
            exporter.export(link)

    # the page given
    def run(self, url, page=-1, form='markdown'):
        self.page = -1
        self.article_list = []
        if page == -1:
            self.getAllArticleUrl(url)
        else:
            page_sum = self.getPageNum(self.get(url))
            if page <= page_sum:
                self.get_one_page_article_url(self.get(url + '/article/list/' + str(page)))
            else:
                print 'page overflow. the sum page of your csdn is ', page_sum
                sys.exit(2)
        PrintLayer.printWorkingPhase('export')
        self.export()
        PrintLayer.printOver()


def parse_to_args():
    parse = argparse.ArgumentParser(description="csdn to hexo")
    parse.add_argument('--name', dest='csdn_name', help='you csdn name', default='')
    parse.add_argument('--type', dest='type', help='enter markdown', default='markdown')
    parse.add_argument('--page', dest='page', help='want to parsed page', default=-1, type=int)
    parse.add_argument('--url', dest='url', help='the parsed article url', default=None)
    return parse.parse_args()


def main():
    args = parse_to_args()
    if args.url is not None:
        exporter = Exporter()
        exporter.export(args.url)
        return
    if args.csdn_name == '':
        print 'Err: need you csdn Username'
        sys.exit(2)
    if args.type != 'markdown':
        print 'Err: markdown or html'
        sys.exit(2)
    url = 'http://blog.csdn.net/' + args.csdn_name
    parser = Parser()
    parser.run(url, args.page, args.type)


if __name__ == "__main__":
    main()
