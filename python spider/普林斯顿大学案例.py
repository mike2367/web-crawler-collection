import requests
from Useragents import ua_list
from lxml import etree
from queue import Queue
import time
from threading import Thread
import random
import csv


class Spider(object):
    def __init__(self):
        self.url = 'https://www.princeton.edu/events?page={}#calendar'
        self.q = Queue()
        self.i = 0

    def get_headers(self):
        headers = {'User-Agents': random.choice(ua_list)}

        return headers

    # url入队列
    def url_in(self):
        for page in range(10):
            url = self.url.format(page)
            self.q.put(url)

    def get_html(self, headers, url):
        html = requests.get(url=url, headers=headers).text

        return html

    def parse_html(self):
        basic_bds = '//div[@class="news-run item"]/a'
        while True:
            # 拿取地址
            if not self.q.empty():
                url = self.q.get()
                headers = self.get_headers()
                html = self.get_html(headers, url)
                parse_obj = etree.HTML(html)
                item = {}
                a_list = parse_obj.xpath(basic_bds)
                for a in a_list:
                    item['link'] = 'https://www.princeton.edu/' + a.xpath('./@href')[0].strip()
                    item['name'] = a.xpath('./h3/text()')[0].strip()
                    item['time'] = a.xpath('./div[@class="subheader"]/text()[2]')[0].strip()
                    item['date'] = a.xpath('./div[@class="subheader"]/div/span[1]/text()')[0].strip() \
                    + '/' + a.xpath('./div[@class="subheader"]/div/span[2]/text()')[0].strip()
                    self.i += 1
                    self.save_csv(item)
                    print('data{}, succeed!'.format(self.i))
            else:
                break

    def save_csv(self, item):
        datas = []
        headers = list(item.keys())
        datas.append(item)
        with open('princeton events reservation.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()# 写入列名
            writer.writerows(datas)# 写入数据

    def run(self):
        self.url_in()
        t_list = []
        # 创建多线程
        for i in range(10):
            t = Thread(target=self.parse_html)
            t_list.append(t)
            t.start()
        for t in t_list:
            t.join()

        print('total:>', self.i)


if __name__ == '__main__':
    start = time.time()
    spider = Spider()
    spider.run()
    end = time.time()
    print("take time:>", end-start)



