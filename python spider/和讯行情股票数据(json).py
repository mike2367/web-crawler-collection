import json
import requests
import random
import time
from Useragents import ua_list
import csv
import cchardet


class Spider(object):
    def __init__(self):
        self.url = "https://stocksquote.hexun.com/a/sortlist?block=2&commodityid=0&title=15&direction=0&start={}&number=50&input=undefined&column=code,name,price,updownrate,LastClose,open,high,low,volume,priceweight,amount,exchangeratio,VibrationRatio,VolumeRatio"
        self.csv_headers = ["code", "name", "price", "updownrate", "LastClose",
                            "open", "high", "low", "volume", "priceweight",
                            "amount", "exchangeratio", "VibrationRatio", "VolumeRatio"]

    def write_headers(self):
        with open('沪深B股.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_headers)
            writer.writeheader()

    def get_headers(self):
        headers = {'User-Agents': random.choice(ua_list)}
        return headers

    def get_html(self, url):
        headers = self.get_headers()
        html = requests.get(url=url, headers=headers)
        encoding = cchardet.detect(html.content)['encoding']
        html = html.content.decode(encoding)[1:-2]

        html = json.loads(html)

        return html

    def save_csv(self, item):
        with open('沪深B股.csv', 'a', newline='', encoding='utf-8') as f:
            datas = [item]
            writer = csv.DictWriter(f, fieldnames=self.csv_headers)
            writer.writerows(datas)

    def parse_json(self, html_json):
        for data in html_json["Data"][0]:
            item = {}
            item['code'] = data[0]
            item['name'] = data[1]
            item['price'] = float(data[2])/100
            item['updownrate'] = float(data[3])/100
            item['LastClose'] = float(data[4])/100
            item['open'] = float(data[5])/100
            item['high'] = float(data[6])/100
            item['low'] = float(data[7])/100
            item['volume'] = float(data[8])/100
            item['priceweight'] = data[9]
            item['amount'] = data[10]
            item['exchangeratio'] = float(data[11])/100
            item['VibrationRatio'] = float(data[12])/100
            item['VolumeRatio'] = float(data[13])/100

            self.save_csv(item)
            print(item)

    def run(self):
        self.write_headers()
        for i in range(0, 57):
            url = self.url.format(i*50)
            html_json = self.get_html(url)
            self.parse_json(html_json)
            time.sleep(random.uniform(1, 2))


if __name__ == "__main__":
    spider = Spider()
    spider.run()






