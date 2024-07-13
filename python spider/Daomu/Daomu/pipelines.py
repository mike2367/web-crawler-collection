# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os


class DaomuPipeline:
    def process_item(self, item, spider):
        directory = r'C:\Bertram Rowen\texts\code\python spider\novel/{}/'.format(item['title'])
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = directory + item['name'] + '.txt'
        with open(filename, 'w') as f:
            f.write(item['content'])

        return item
