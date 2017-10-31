import csv
import os
import re
import time

import pandas as pd
import selenium.webdriver as webdriver
from lxml import html

from Models import Data_Models


class Oscar_Wilson:

    def __init__(self):
        self.userName = "9313"
        self.password = "3622elm"
        self.productIdsFilePath = r'T:/ebay/mtd/inventory/ProductIds.csv'
        self.resultsFilePath = r'T:/ebay/mtd/inventory/'
        self.loginUrl = "http://69.29.127.5:8080/u650ow/servlet/se.ibs.ns.cf.StartServlet?page=sign-on"
        self.userNameXPath = r'/html/body/form/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td[2]/input'
        self.passwordXPath = r'/html/body/form/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/div/table/tbody/tr[3]/td[2]/input'
        self.loginClickXPath = r'/html/body/form/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/div/table/tbody/tr[5]/td[2]/input[1]'
        self.productDataSet = self.getDataSet()
        self.headerRow = ["Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action"]

    def scrape(self):
        global browser
        dateStr = time.strftime("%m%d%Y"+'.'+"%I%M")
        results = self.resultsFilePath+'MTDScrape' + dateStr + '.csv'
        browser = webdriver.Chrome()
        dataSet = self.getDataSet()
        self.login()
        refreshCounter = 0
        with open(results, 'a', newline='') as f:
            global writer
            writer = csv.writer(f)
            writer.writerow(self.headerRow)
            count = 0
            total = sum(1 for row in dataSet.iterrows())
            for index, row in dataSet.iterrows():

                if refreshCounter >= 500:
                    browser.quit()
                    browser = webdriver.Chrome()
                    self.login()
                    refreshCounter = 0
                dataFrame = Data_Models.ResultsForEbay(row)
                productID = dataFrame.productID
                time.sleep(1)
                self.loadProduct(productID)
                html = self.gethtml()
                # try:
                # availQty = self.parse(html)
                # dataFrame.quantity = availQty
                # # except:
                # #     dataFrame.quantity = 'invalid'
                # dataFrame.getFrameAsList()
                # self.saveRecord(dataFrame.frameAsList)
                refreshCounter += 1
                self.cls()
                print(str(int((count / total) * 100)) + '%')
                count += 1
        browser.quit()

    def getDataSet(self):
        ds = pd.read_csv(self.productIdsFilePath, dtype=object, na_filter=False)
        return (ds)

    def login(self):
        userName = self.userName
        password = self.password
        loginUrl = self.loginUrl
        userNameXpath = self.userNameXPath
        passwordXpath = self.passwordXPath
        loginClickXPath = self.loginClickXPath
        browser.get(loginUrl)
        try:
            main_frame = browser.find_element_by_xpath(r'//*[@id="innerFr"]/frame[2]')
            browser.switch_to.frame(main_frame)
            browser.find_element_by_xpath(userNameXpath).send_keys(userName)
            browser.find_element_by_xpath(passwordXpath).send_keys(password)
            browser.find_element_by_xpath(loginClickXPath).click()
        except:
            pass

    def loadProduct(self, partNumber):
        currentWindow = browser.current_window_handle
        header_frame = browser.find_element_by_xpath(r'//*[@id="innerFr"]/frame[1]')
        browser.switch_to.frame(header_frame)
        try:
            browser.find_element_by_xpath(r'/html/body/div/div[1]').click()
        except:
            try:
                browser.find_element_by_xpath(r'/html/body/div[4]/div[1]').click()
            except:
                try:
                    browser.find_element_by_xpath(r'/html/body/div[6]/div[1]').click()
                except:
                    browser.find_element_by_xpath(r'/html/body/div[8]/div[1]').click()

        browser.switch_to.window(currentWindow)
        part_search_frame = browser.find_element_by_xpath(r'//*[@id="innerFr"]/frame[2]')
        browser.switch_to.frame(part_search_frame)
        partNumberXPath = '/html/body/form/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[8]/td/table/tbody/tr[3]/td[2]/input'
        submitButtonXPath1 = r'/html/body/form/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[8]/td/table/tbody/tr[4]/td[2]/input'
        submitButtonXPath2 = r'/html/body/form/div/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[10]/td/table/tbody/tr[4]/td[2]/input'
        browser.find_element_by_xpath(partNumberXPath).send_keys(partNumber)
        try:
            browser.find_element_by_xpath(submitButtonXPath1).click()
        except:
            browser.find_element_by_xpath(submitButtonXPath2).click()
        html_scrape = browser.page_source
        tree = html.fromstring(html_scrape)
        results_table = tree.xpath(r'//*[@id="item-search-table"]/tbody')
        i=1
        try:
            for row in results_table[0]:
                for td in row:
                    for element in td:
                        elementString = str(' '.join(str(element.text).split())).replace('None', '')
                        if elementString:
                            if elementString == 'MTD'+partNumber:
                                browser.find_element_by_xpath(r'//*[@id="item-search-table"]/tbody/tr['+str(i)+']/td[1]/a').click()
                                break
                        else:
                            continue
                i += 1
        except:
            pass
        browser.switch_to.window(currentWindow)

    def gethtml(self):
        return (browser.page_source)

    def parse(self, htmlScrape):
        tree = html.fromstring(htmlScrape)
        qty_mn = tree.xpath('//*[@id="idBackDrop"]/tbody/tr[3]/td[1]/table/tbody/tr[4]/td/table/tbody/tr[7]/td/table/tbody/tr[1]/td[2]/text()')[0]
        qty_wi = tree.xpath('//*[@id="idBackDrop"]/tbody/tr[3]/td[1]/table/tbody/tr[4]/td/table/tbody/tr[7]/td/table/tbody/tr[2]/td[2]/text()')[0]
        if qty_mn == 'In Stock':
            qty_mn = 100
        else:
            qty_mn = re.sub(r'[^0-9]','',qty_mn)
        if qty_wi == 'In Stock':
            qty_wi = 100
        else:
            qty_wi = re.sub('[^0-9]','',qty_wi)
        if qty_mn == '':
            qty_mn = 0
        if qty_wi == '':
            qty_wi = 0
        qty = int(qty_wi) + int(qty_mn)
        return (qty)

    def saveRecord(self, dataFrame):
        writer.writerow(dataFrame)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')