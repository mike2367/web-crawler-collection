import pymysql
import requests
import json
import random
import time
from Useragents import ua_list

# http://www.santostang.com/
class Spider(object):
    # 通过搜索评论内容快速获得评论数据包
    def __init__(self):
        self.url = 'https://api-zero.livere.com/v1/comments/list?callback=jQuery112408682037701495582_1714279915663&limit={}&repSeq=4290319&requestPath=%2Fv1%2Fcomments%2Flist&consumerSeq=1020&livereSeq=28583&smartloginSeq=5154&code=&_=1714279915665'
        self.db = pymysql.connect(
            host='localhost', user='root', password='123456',
            database='commentsdb', charset='utf8mb4'
        )
        self.cursor = self.db.cursor()
        self.comments = []

    def get_headers(self):
        headers = {'User-Agent': random.choice(ua_list)}
        return headers

    def get_json(self, url):
        json_string = requests.get(url=url, headers=self.get_headers()).text
        json_string = json_string[json_string.find('{'):-2]
        html_json = json.loads(json_string)

        return html_json

    def parse_json(self, html_json):
        comment_list = html_json["results"]['parents']
        print(comment_list)
        for reply in comment_list:
            user = reply["name"]
            content = reply["content"]

            self.comments.append([user, content])

    def search(self):
        url = self.url.format(1)
        html_json = self.get_json(url)
        first_comment = html_json["results"]['parents'][0]["content"]
        sel = 'select comment from version where comment=%s'
        result = self.cursor.execute(sel, [first_comment])
        if result:
            print("网站未更新")
        else:
            time.sleep(random.uniform(2, 3))
            url = self.url.format(50)
            html_json = self.get_json(url)
            self.parse_json(html_json)

            self.insert_mysql()
            dele = 'delete from version'
            ins = 'insert into version values(%s)'
            self.cursor.execute(dele)
            self.cursor.execute(ins, [first_comment])
            self.db.commit()

    def insert_mysql(self):
        dele = 'delete from comments'
        self.cursor.execute(dele)

        ins = 'insert into comments values(%s, %s)'
        self.cursor.executemany(ins, self.comments)

    def run(self):
        self.search()


if __name__ == "__main__":
    spider = Spider()
    spider.run()