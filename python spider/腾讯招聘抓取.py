# 抓取职位名称，工作职责
# 从一级页面中提取postid
# 二级页面提取信息
import requests
import json
import random
import time
from Useragents import ua_list
from urllib import parse


class Spider(object):
    def __init__(self):
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1674630712030&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=16452693&postId={}&language=zh-cn'

    def get_headers(self):
        headers = {'User-Agent': random.choice(ua_list)}
        return headers

    # 获取json数据
    def get_json(self, url):
        html_json = requests.get(url=url, headers=self.get_headers()).text
        html_json = json.loads(html_json)

        return html_json

    # 解析数据
    def parse(self, one_url):
        one_html = self.get_json(one_url)
        for one in one_html['Data']['Posts']:
            post_id = one['PostId']
            two_url = self.two_url.format(post_id)
            self.parse_two_page(two_url)

    def parse_two_page(self, two_url):
        two_html = self.get_json(two_url)
        item = {}
        item['name'] = two_html['Data']['RecruitPostName'].strip('\n').replace('\r\n', "")
        item['requirement'] = two_html['Data']['Requirement'].strip('\n').replace('\r\n', "")
        item['responsibility'] = two_html['Data']['Responsibility'].strip('\n').replace('\r\n', "")
        print(item)

    def get_total(self, keyword):
        html = self.get_json(self.one_url.format(keyword, 1))
        total = html['Data']['Count']
        total = round(int(total) / 10)

        return total

    def run(self):
        keyword = input('search the position')
        # url编码操作
        keyword = parse.quote(keyword)
        total = self.get_total(keyword)
        for i in range(1, total):
            try:
                url = self.one_url.format(keyword, i)
                self.parse(url)
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                continue


if __name__ == '__main__':
    spider = Spider()
    spider.run()