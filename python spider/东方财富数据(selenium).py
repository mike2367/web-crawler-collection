from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import csv
from schedule import every, run_pending, repeat


class Spider(object):
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        self.url = 'https://data.eastmoney.com/bbsj/202206/lrb.html'
        self.browser = webdriver.Firefox(options=options)
        self.i = 0
        self.faliure = 0
        self.headers = ['股票简称', '股票代码', '净利润', '利润同比', '营业总收入', '营业总收入同比', '营业支出', '销售费用', '管理费用', '财务费用', '营业总支出', '营业利润', '利润总额']

    def open_csv(self):
        with open('东方财富.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()

    def get_html(self):
        base_xpath = '//div[@class="dataview-body"]//tbody/tr'
        name_xpath = './/a/span'
        code_xpath = './td[2]/a'
        gain_xpath = './td[5]'
        element = self.browser.find_elements(by=By.XPATH, value=base_xpath)
        for tr in element:
            item = {}
            item['股票简称'] = tr.find_element(by=By.XPATH, value=name_xpath).text.strip()
            item['股票代码'] = tr.find_element(by=By.XPATH, value=code_xpath).text.strip()
            item['净利润'] = tr.find_element(by=By.XPATH, value=gain_xpath).text.strip()
            item['利润同比'] = tr.find_element(by=By.XPATH, value='./td[6]').text.strip()
            item['营业总收入'] = tr.find_element(by=By.XPATH, value='./td[7]').text.strip()
            item['营业总收入同比'] = tr.find_element(by=By.XPATH, value='./td[8]').text.strip()
            item['营业支出'] = tr.find_element(by=By.XPATH, value='./td[9]').text.strip()
            item['销售费用'] = tr.find_element(by=By.XPATH, value='./td[10]').text.strip()
            item['管理费用'] = tr.find_element(by=By.XPATH, value='./td[11]').text.strip()
            item['财务费用'] = tr.find_element(by=By.XPATH, value='./td[12]').text.strip()
            item['营业总支出'] = tr.find_element(by=By.XPATH, value='./td[13]').text.strip()
            item['营业利润'] = tr.find_element(by=By.XPATH, value='./td[14]').text.strip()
            item['利润总额'] = tr.find_element(by=By.XPATH, value='./td[15]').text.strip()
            self.save_csv(item)

    def page_change(self):
        button = self.browser.find_element(by=By.XPATH, value='//*[@id="dataview"]/div[3]/div[1]/a[last()]')
        button.click()

    def save_csv(self, item):
        datas = []
        datas.append(item)
        with open('东方财富.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerows(datas)

    @repeat(every().day.at("12:00"))
    def run(self):
        self.open_csv()
        url = self.url
        self.browser.get(url)
        while self.i < 99:
            try:
                self.get_html()
                page = self.browser.find_element(by=By.XPATH, value='//div[@class="pagerbox"]/a[@class="active"]').text
                print("page{}, success".format(page))
                time.sleep(random.uniform(1, 2))
                self.page_change()
                self.i += 1
            except Exception as e:
                self.faliure += 1
                continue

        print('{}faliure'.format(self.faliure))


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    while True:
        run_pending()
        time.sleep(1)




