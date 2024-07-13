from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import csv


class Spider(object):
    def __init__(self):
        self.url = 'https://finviz.com/screener.ashx?v=110&s=ta_unusualvolume'
        self.browser = webdriver.Chrome()
        self.page = 0
        self.total = 0
        self.failure = 0
        self.headers = ['Ticker', 'Tickerlink', 'Company', 'Sector', 'Industry', 'Country', 'Market Cap', 'P/E', 'Price', 'Change', 'Volume']

    def open_csv(self):
        with open("stock unusual volume.csv", 'a', newline='', encoding='utf-8')as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()

    def get_html(self):
        base_xpath = '//div[@id="screener-content"]//tbody/tr[@valign="top"]'
        element = self.browser.find_elements(by=By.XPATH, value=base_xpath)
        for tr in element:
            item = {}
            item['Ticker'] = tr.find_element(by=By.XPATH, value='.//td[2]/a').text.strip()
            item['Tickerlink'] = tr.find_element(by=By.XPATH, value='.//td[2]/a').get_attribute('href').strip()
            item['Company'] = tr.find_element(by=By.XPATH, value='.//td[3]/a').text.strip()
            item['Sector'] = tr.find_element(by=By.XPATH, value='.//td[4]/a').text.strip()
            item['Industry'] = tr.find_element(by=By.XPATH, value='.//td[5]/a').text.strip()
            item['Country'] = tr.find_element(by=By.XPATH, value='.//td[6]/a').text.strip()
            item['Market Cap'] = tr.find_element(by=By.XPATH, value='.//td[7]/a').text.strip()
            item['P/E'] = tr.find_element(by=By.XPATH, value='.//td[8]/a').text.strip()
            item['Price'] = tr.find_element(by=By.XPATH, value='.//td[9]/a').text.strip()
            item['Change'] = tr.find_element(by=By.XPATH, value='.//td[10]/a').text.strip()
            item['Volume'] = tr.find_element(by=By.XPATH, value='.//td[11]/a').text.strip()
            self.total += 1
            self.save_csv(item)

    def save_csv(self, item):
        datas = []
        datas.append(item)
        with open('stock unusual volume.csv', 'a', newline='', encoding='utf-8')as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerows(datas)

    def page_change(self):
        if self.page == 0:
            button = self.browser.find_element(by=By.XPATH, value='//*[@id="screener-views-table"]/tbody/tr[7]/td/a[11]')
        else:
            button = self.browser.find_element(by=By.XPATH, value='//*[@id="screener-views-table"]/tbody/tr[7]/td/a[12]')
        button.click()

    def run(self):
        self.open_csv()
        url = self.url
        self.browser.get(url)
        while self.page < 10:
            try:
                self.get_html()
                if self.page == 0:
                    page = 1
                else:
                    page = self.browser.find_element(by=By.XPATH, value='//*[@id="screener-views-table"]/tbody/tr[7]/td/a[@class="tab-link"][2]').text

                if self.page == 9:
                    self.page += 1
                else:
                    self.page_change()
                    self.page += 1
                print("page{}, succeeded".format(page))
                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(e)
                self.failure += 1
                continue

        print("{} failure".format(self.failure))
        print("total number: ", self.total)


if __name__ == "__main__":
    spider = Spider()
    begin = time.time()
    spider.run()
    end = time.time()
    print("take time: ", end-begin)