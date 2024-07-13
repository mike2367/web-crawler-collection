# 先在数据库中建表，分为省，市，区三等级，分别记录号码
# 先于数据库中的原始内容比对，若有更新则删除之前的数据，重新爬取并插入
from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql


class Spider(object):
    def __init__(self):
        self.url = 'https://www.mca.gov.cn/article/sj/xzqh/2019/'
        # 设置为无界面
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.db = pymysql.connect(
            host='localhost', user='root', password='123456',
            database='govdb', charset='utf8mb4'
        )
        self.cursor = self.db.cursor()
        # 创建三个大列表，为executemany使用
        self.province = []
        self.city = []
        self.county = []

    def get_data(self):
        self.browser.get(self.url)
        xpath_bds = '//td[@class="arlisttd"]/a[contains(@title, "行政区划代码")]'
        a = self.browser.find_element(by=By.XPATH, value=xpath_bds)
        href = a.get_attribute('href')# 获取一个节点的属性值
        # 在version表查询，得到结果result
        sel = 'select url from version where url=%s'
        # result返回受影响的条数
        result = self.cursor.execute(sel, [href])# 列表传参
        if result:
            print('网站未更新')
        else:
            a.click()
            self.get_code()
            # 把href插入到version表中
            dele = 'delete from version'
            ins = 'insert into version values(%s)'
            self.cursor.execute(dele)
            self.cursor.execute(ins, [href])
            self.db.commit()

    def get_code(self):
        # 切换句柄
        all_handles = self.browser.window_handles
        self.browser.switch_to.window(all_handles[1])
        # 开始抓数据
        xpath_bds = '//tr[@height="19"]'
        tr_list = self.browser.find_elements(by=By.XPATH, value=xpath_bds)
        for tr in tr_list:
            code = tr.find_element(by=By.XPATH, value='./td[2]').text.strip()
            name = tr.find_element(by=By.XPATH, value='./td[3]').text.strip()
            print(name, code)

            # 根据等级分类
            if code[-4:] == '0000':
                self.province.append([name, code])
                # 额外添加四个直辖市
                if name in ['北京市', '天津市', '上海市', '重庆市']:
                    self.city.append([name, code, code])
            elif code[-2:] == '00':
                self.city.append([name, code, code[:2] + '0000'])# 省编号后四位都为0
            else:
                if code[:2] in ['11', '12', '31', '50']:
                    self.county.append([name, code, code[:2] + '0000'])
                else:
                    self.county.append([name, code, code[:4] + '00'])

        self.insert_mysql()

    def insert_mysql(self):
        # 先清空表
        del1 = 'delete from province'
        del2 = 'delete from city'
        del3 = 'delete from county'
        self.cursor.execute(del1)
        self.cursor.execute(del2)
        self.cursor.execute(del3)
        # 再插入新数据
        ins1 = 'insert into province values(%s,%s)'
        ins2 = 'insert into city values(%s,%s,%s)'
        ins3 = 'insert into county values(%s,%s,%s)'
        self.cursor.executemany(ins1, self.province)
        self.cursor.executemany(ins2, self.city)
        self.cursor.executemany(ins3, self.county)

    def run(self):
        self.get_data()


if __name__ == '__main__':
    spider = Spider()
    spider.run()

