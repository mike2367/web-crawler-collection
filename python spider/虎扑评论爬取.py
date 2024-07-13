import requests
import random
import time
from lxml import etree
from Useragents import ua_list

class Spider(object):
    def __init__(self):
        self.url = "https://bbs.hupu.com/626409291-{}.html"

    def get_headers(self):
        headers = {"User-Agent": random.choice(ua_list)}
        return headers

    def get_html(self, url):
        headers = self.get_headers()
        html = requests.get(url=url, headers=headers).text
        return html

    def parse_html(self, html):
        base_xpath = '//div[@class="post-wrapper_bbs-post-wrapper__UdhwQ post-wrapper_gray__HNv4A"]' \
                     '//div[@class="thread-content-detail"]/p/text()'
        parse_html = etree.HTML(html)
        text_list = parse_html.xpath(base_xpath)
        print(text_list)


    def run(self):
        for i in range(3):
            index = i + 1
            url = self.url.format(index)
            html = self.get_html(url)
            self.parse_html(html)
            time.sleep(random.uniform(1,2))

if __name__ == "__main__":
    spider = Spider()
    spider.run()