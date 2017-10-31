from Classes import Distributor, User_Info
from lxml import html
import time
import re

class AIP(Distributor.Scrape_Distributor):

    def __init__(self, manufacturer):
        super(AIP, self).__init__(manufacturer)

    def login(self, browser):
        login_url = r'https://' + self.username + ':' + self.password + '@www.aiproducts.com/dealer/customer.htm'
        browser.get(login_url)
        frameXPath = '/html/frameset/frameset/frame[1]'
        menuXPath = '/html/body/a[2]/p'
        subMenuXPath = '//*[@id="sub1"]/a[2]'
        frame = browser.find_element_by_xpath(frameXPath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(menuXPath).click()
        browser.find_element_by_xpath(subMenuXPath).click()

    def load_product(self, product_id, browser):
        browser.switch_to.default_content()
        frame_xpath = r'/html/frameset/frameset/frame[2]'
        item_number_input_xpath = r'//html/body/form/table/tbody/tr/td[1]/table/tbody/tr[1]/td[3]/input'
        qty_input_xpath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[1]'
        check_button_xpath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[2]'
        frame = browser.find_element_by_xpath(frame_xpath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(item_number_input_xpath).clear()
        browser.find_element_by_xpath(item_number_input_xpath).send_keys(product_id.strip('[]'))
        browser.find_element_by_xpath(qty_input_xpath).clear()
        browser.find_element_by_xpath(qty_input_xpath).send_keys('10')
        browser.find_element_by_xpath(check_button_xpath).click()

    def parse_scrape(self, item, htmlScrape):
        tree = html.fromstring(htmlScrape)
        adjustTR = 0
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[10]/td/img'):
            adjustTR = 1
        if (tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[14]/td[1]/text()')[0]) == ':':
            item['Quantity'] = 'invalid'
            return (item)
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[11]/td/table/tbody/tr[2]/td[2]/input'):
            item['Quantity'] ='vendor dropship'
            return (item)
        IA = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 10) + ']/td[3]/text()')[
                0])
        IN = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 11) + ']/td[3]/text()')[
                0])
        MO = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 12) + ']/td[3]/text()')[
                0])
        NC = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 13) + ']/td[3]/text()')[
                0])
        TX = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 14) + ']/td[3]/text()')[
                0])
        CA = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 15) + ']/td[3]/text()')[
                0])
        WA = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 16) + ']/td[3]/text()')[
                0])
        PA = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 17) + ']/td[3]/text()')[
                0])
        GA = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 18) + ']/td[3]/text()')[
                0])
        FL = int(
            tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' + str(adjustTR + 19) + ']/td[3]/text()')[
                0])
        qty = IA + IN + MO + NC + TX + CA + WA + PA + GA + FL
        item['Quantity'] = qty
        return (item)