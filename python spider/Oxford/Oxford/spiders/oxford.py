import scrapy
from ..items import OxfordItem


class OxfordSpider(scrapy.Spider):
    name = "oxford"
    allowed_domains = ["www.ox.ac.uk"]
    start_url = "https://www.ox.ac.uk/events-list?page={}"

    def start_requests(self):
        for i in range(1, 22):
            url = self.start_url.format(i)
            yield scrapy.Request(
               url=url,
               callback=self.parse_first_image
           )

    def parse_first_image(self, response):
        a_list = response.xpath('//*[@id="main-content"]//div[2]/h2/a')
        for a in a_list:
            item = OxfordItem()
            item['title'] = a.xpath('./text()').get()
            url = a.xpath('./@href').get()
            url = 'https://www.ox.ac.uk' + url
            yield scrapy.Request(
                url=url,
                meta={'item': item},
                callback=self.parse_two_page
            )

    def parse_two_page(self, response):
        main = response.xpath('//*[@id="node-event-oxweb-full-content-group-event-meta"]')
        try:
            date = main.xpath('./div[2]/span/span/span/text()').get()
        except Exception as e:
            date = 'None'
        try:
            time = main.xpath('./div[3]/span/div/text()').get().strip('\n')
        except Exception as e:
            time = main.xpath('./div[4]/span/div/text()').get().strip('\n')
        try:
            telephone = response.xpath('//*[@id="main-content"]/div/div[2]/span/p/text()[2]').get()
        except Exception as e:
            telephone = 'None'
        content = response.xpath('//*[@id="main-content"]/div/div[2]/span/p/text()[1]').get()
        item = response.meta['item']

        item['date'] = date
        item['time'] = time
        item['telephone'] = telephone
        item['content'] = content

        yield item
