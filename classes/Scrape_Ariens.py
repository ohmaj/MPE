from classes import ABC_Distributor_Scrape
from lxml import html
import re
from selenium.webdriver.support.ui import Select


class Ariens(ABC_Distributor_Scrape.DistributorScrape):

    def __init__(self, manufacturer):
        super(Ariens, self).__init__(manufacturer)
        self.manufacturer = manufacturer
        self.login_url = r'http://connect.ariens.com/cgibin/pnrg0099d'

    def login(self):
        browser = self.browser
        username = self.username
        password = self.password
        loginUrl = self.login_url
        username_xpath = r'//*[@id="body"]/form/table/tbody/tr[2]/td/input'
        password_xpath = r'//*[@id="body"]/form/table/tbody/tr[4]/td/input'
        login_click_xpath = r'//*[@id="body"]/form/table/tbody/tr[8]/td[2]/input[1]'
        browser.get(loginUrl)
        browser.find_element_by_xpath(username_xpath).send_keys(username)
        browser.find_element_by_xpath(password_xpath).send_keys(password)
        browser.find_element_by_xpath(login_click_xpath).click()

    def load_product(self, product_id, browser):
        productSearchUrl = r'http://connect.ariens.com/cgibin/pnrg0099f?dmcust=78919678Browser=NetscapeVersion=5.0%20' \
                           r'Screen=1920x1080Level=AG011000000Program=/cgibin/gprg0248'
        partNumberXPath = '/html/body/form/table[2]/tbody/tr[1]/td[3]/input'
        qtyXPath = '/html/body/form/table[2]/tbody/tr[3]/td[3]/input'
        submitButtonXPath = r'/html/body/form/center/input[2]'
        frameXPath = r'/html/frameset/frame[2]'
        browser.get(productSearchUrl)
        frame = browser.find_element_by_xpath(frameXPath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(partNumberXPath).send_keys(product_id.strip("[]"))
        browser.find_element_by_xpath(qtyXPath).send_keys('10')
        browser.find_element_by_xpath(submitButtonXPath).click()
        try:
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[4]/text()')
        except:
            browser.get(productSearchUrl)
            frame = browser.find_element_by_xpath(frameXPath)
            browser.switch_to.frame(frame)
            browser.find_element_by_xpath(partNumberXPath).send_keys(product_id.strip("[]"))
            browser.find_element_by_xpath(qtyXPath).send_keys('10')
            select = Select(browser.find_element_by_name('partid'))
            select.select_by_visible_text('Gravely')
            browser.find_element_by_xpath(submitButtonXPath).click()


    def parse_scrape(self, item, html_scrape):
        tree = html.fromstring(html_scrape)
        qty = tree.xpath('/html/body/table[2]/tbody/tr[2]/td[4]/text()')
        if len(qty) < 1:
            item['Quantity'] = 'invalid part number'
        else:
            qty = re.sub('[^0-9]', '', qty[0])
            item['Quantity'] = qty
        return item
