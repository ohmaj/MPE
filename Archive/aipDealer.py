import csv
import os
import time

import pandas as pd
import selenium.webdriver as webdriver
from lxml import html

from Models import Data_Models


class AIP:

    def __init__(self):
        self.userName = "IL7660"
        self.password = "3622elm"
        self.productIdsFilePath = r'T:/ebay/AIP/inventory/ProductIds.csv'
        self.resultsFilePath = r'T:/ebay/AIP/inventory/AIPScrape' + time.strftime("%m%d%Y"+'.'+"%I%M") + '.csv'
        self.loginUrl = r'https://'+self.userName+':'+self.password+'@www.aiproducts.com/dealer/customer.htm'
        self.productDataSet = self.getDataSet()
        self.headerRow = ["Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action"]

    def get_update(self):
        global browser
        browser = webdriver.Chrome()
        dataSet = self.getDataSet()
        self.login()
        with open(self.resultsFilePath, 'a', newline='') as f:
            global writer
            writer = csv.writer(f)
            writer.writerow(self.headerRow)
            count = 0
            total = sum(1 for row in dataSet.iterrows())
            for index, row in dataSet.iterrows():
                dataFrame = Data_Models.ResultsForEbay(row)
                productID = dataFrame.productID.strip("[]")
                self.loadProduct(browser, productID, 10)
                html = self.gethtml()
                availQty = self.parse(html)
                dataFrame.quantity = availQty
                dataFrame.fulfillmentSource = "Drop Shipper"
                dataFrame.supplierName = 'A&I Products'
                dataFrame.supplierAccountNum = 'IL7660'
                dataFrame.supplierID = '12'
                dataFrame.getFrameAsList()
                self.saveRecord(dataFrame.frameAsList)
                self.cls()
                print('A&I Progress: '+str(int((count / total) * 100)) + '%')
                count += 1
        browser.quit()

    def getDataSet(self):
        ds = pd.read_csv(self.productIdsFilePath, dtype=object, na_filter=False)
        return (ds)

    def login(self):
        loginUrl = self.loginUrl
        browser.get(loginUrl)
        frameXPath = '/html/frameset/frameset/frame[1]'
        menuXPath = '/html/body/a[2]/p'
        subMenuXPath = '//*[@id="sub1"]/a[2]'
        frame = browser.find_element_by_xpath(frameXPath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(menuXPath).click()
        browser.find_element_by_xpath(subMenuXPath).click()

    def loadProduct(self, browser, partNumber, qty):
        browser.switch_to.default_content()
        frameXPath = r'/html/frameset/frameset/frame[2]'
        itemNumberInputXPath = r'//html/body/form/table/tbody/tr/td[1]/table/tbody/tr[1]/td[3]/input'
        qtyInputXPath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[1]'
        checkButtonXPath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[2]'
        frame = browser.find_element_by_xpath(frameXPath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(itemNumberInputXPath).clear()
        browser.find_element_by_xpath(itemNumberInputXPath).send_keys(partNumber)
        browser.find_element_by_xpath(qtyInputXPath).clear()
        browser.find_element_by_xpath(qtyInputXPath).send_keys(qty)
        browser.find_element_by_xpath(checkButtonXPath).click()

    def gethtml(self):
        return (browser.page_source)

    def parse(self, htmlScrape):
        tree = html.fromstring(htmlScrape)
        adjustTR = 0
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[10]/td/img'):
            adjustTR = 1
        if (tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[14]/td[1]/text()')[0]) == ':':
            return ('invalid')
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[11]/td/table/tbody/tr[2]/td[2]/input'):
            return ('vendor dropship')
        IA = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+10)+']/td[3]/text()')[0])
        IN = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+11)+']/td[3]/text()')[0])
        MO = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+12)+']/td[3]/text()')[0])
        NC = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+13)+']/td[3]/text()')[0])
        TX = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+14)+']/td[3]/text()')[0])
        CA = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+15)+']/td[3]/text()')[0])
        WA = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+16)+']/td[3]/text()')[0])
        PA = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+17)+']/td[3]/text()')[0])
        GA = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+18)+']/td[3]/text()')[0])
        FL = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr['+str(adjustTR+19)+']/td[3]/text()')[0])
        qty = IA+IN+MO+NC+TX+CA+WA+PA+GA+FL
        return (qty)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def saveRecord(self, dataFrame):
        writer.writerow(dataFrame)



