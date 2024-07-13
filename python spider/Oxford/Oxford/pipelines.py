# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class OxfordPipeline:
    def __init__(self):
        self.headers = ['title', 'date', 'time', 'telephone', 'content']

    def open_csv(self):
        with open('oxford.csv', 'a', newline='', encoding='utf-8')as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()

    def process_item(self, item, spider):
        datas = []
        datas.append(item)
        with open('oxford.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerows(datas)

        return item
