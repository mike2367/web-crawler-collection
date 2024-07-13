import requests
from Useragents import ua_list
import time
import random
from lxml import etree


class Spider(object):
    def __init__(self):
        self.url = 'https://kms.shanghaitech.edu.cn/simple-search?rpp=10&&start={}'

    def get_headers(self):
        headers = {'User-Agent': random.choice(ua_list)}
        return headers

    def get_html(self, url, headers):
        for i in range(10):
            try:
                html = requests.get(url=url, headers=headers).text
                print('get html succeeded')
                return html
            except Exception as e:
                continue

    def parse_html(self, html):
        parse_obj = etree.HTML(html)

        # 基准匹配
        xpath_bds1 = '//form[@name="itemlist"]//td[@width="750"]'
        tr_list = parse_obj.xpath(xpath_bds1)
        item = {}
        for tr in tr_list:
            item['name'] = tr.xpath('./span[1]/a[1]/strong/text()')[0].strip()
            item['type'] = tr.xpath('./span[1]/a[2]/text()')[0].strip()
            item['link'] = 'https://kms.shanghaitech.edu.cn/' + tr.xpath('./span[1]/a[1]/@href')[0].strip()
            print(item)

    def run(self):
        for i in range(0, 145):
            url = self.url.format(i * 10)
            headers = self.get_headers()
            html = self.get_html(url, headers)
            self.parse_html(html)
            print("page:>{},succeed".format(i))
            time.sleep(random.uniform(1, 3))


if __name__ == "__main__":
    spider = Spider()
    spider.run()
