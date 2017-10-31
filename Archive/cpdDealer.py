import csv
import re
import time

import pandas as pd
import selenium.webdriver as webdriver
from lxml import html

from Models import Data_Models


class CPD:

    def __init__(self, mfr):
        self.userName = "22462"
        self.password = "3622elmst"
        self.mfr = mfr
        self.productIdsFilePath = r'T:/ebay/'+mfr+'/inventory/ProductIds.csv'
        self.resultsFilePath = r'T:/ebay/'+mfr+'/inventory/'
        self.loginUrl = "https://ezone.cpdonline.com/cgi-bin/edmas8a.mac/initialindex"
        self.userNameXPath = r'//*[@id="idFrmSignIn"]/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/input'
        self.passwordXPath = r'//*[@id="idFrmSignIn"]/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/input'
        self.loginClickXPath = r'//*[@id="idFrmSignIn"]/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[4]/td/input'
        self.productSearchUrl = r'https://ezone.cpdonline.com/cgi-bin/edmas8a.mac/ItemSearchBegin'
        self.productDataSet = self.getDataSet()
        self.headerRow = ["Title","Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action"]

    def scrape(self):
        global browser
        dateStr = time.strftime("%m%d%Y"+'.'+"%I%M")
        results = self.resultsFilePath+self.mfr+'Scrape' + dateStr + '.csv'
        browser = webdriver.Chrome()
        dataSet = self.getDataSet()
        self.login()
        refreshCounter = 0
        with open(results, 'a', newline='') as f:
            global writer
            writer = csv.writer(f)
            writer.writerow(self.headerRow)
            for index, row in dataSet.iterrows():

                if refreshCounter >= 500:
                    browser.quit()
                    browser = webdriver.Chrome()
                    self.login()
                    refreshCounter = 0
                dataFrame = Data_Models.ResultsForEbay(row)
                productID = dataFrame.productID
                self.loadProduct(productID, 100)
                html = self.gethtml()
                try:
                    availQty = self.parse(html)
                    dataFrame.fulfillmentSource = "Drop Shipper"
                    dataFrame.quantity = availQty
                except:
                    try:
                        multi_results_part_id = browser.find_element_by_xpath(r'//*[@id="tblResults"]/tbody/tr[2]/td[8]')
                        multi_results_part_id = str(multi_results_part_id.text).rstrip(' ')
                        multi_results_click = r'//*[@id="tblResults"]/tbody/tr[2]/td[6]/a'
                        if multi_results_part_id == str(productID).rstrip(' '):
                            browser.find_element_by_xpath(multi_results_click).click()
                            html = self.gethtml()
                            availQty = self.parse(html)
                            dataFrame.quantity = availQty
                        else:
                            multi_results_part_id = browser.find_element_by_xpath(
                                r'//*[@id="tblResults"]/tbody/tr[3]/td[8]')
                            multi_results_part_id = str(multi_results_part_id.text).rstrip(' ')
                            multi_results_click = r'//*[@id="tblResults"]/tbody/tr[3]/td[6]/a'
                            if multi_results_part_id == str(productID).rstrip(' '):
                                browser.find_element_by_xpath(multi_results_click).click()
                                html = self.gethtml()
                                availQty = self.parse(html)
                                dataFrame.quantity = availQty
                            else:
                                dataFrame.quantity = 'Part Id Needs Review'

                    except:
                        dataFrame.quantity = 'invalid'

                dataFrame.getFrameAsList()
                self.saveRecord(dataFrame.frameAsList)
                refreshCounter += 1
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
            browser.find_element_by_xpath(userNameXpath).send_keys(userName)
            browser.find_element_by_xpath(passwordXpath).send_keys(password)
            browser.find_element_by_xpath(loginClickXPath).click()
        except:
            pass

    def loadProduct(self, partNumber, qty):
        productSearchUrl = self.productSearchUrl
        partNumberXPath = '//*[@id="ITNBR"]'
        qtyXPath = '//*[@id="QTYOR"]'
        submitButtonXPath = r'//*[@id="mainFull"]/table[1]/tbody/tr[3]/td/table/tbody/tr[4]/td/input[2]'
        browser.get(productSearchUrl)
        browser.find_element_by_xpath(partNumberXPath).send_keys(partNumber)
        browser.find_element_by_xpath(qtyXPath).send_keys(qty)
        browser.find_element_by_xpath(submitButtonXPath).click()

    def gethtml(self):
        return (browser.page_source)

    def parse(self, htmlScrape):
        tree = html.fromstring(htmlScrape)
        qty_mn = tree.xpath('//*[@id="idBackDrop"]/tbody/tr[3]/td[1]/table/tbody/tr[4]/td/table/tbody/tr[7]/td/table/tbody/tr[1]/td[2]/text()')[0]
        qty_wi = tree.xpath('//*[@id="idBackDrop"]/tbody/tr[3]/td[1]/table/tbody/tr[4]/td/table/tbody/tr[7]/td/table/tbody/tr[2]/td[2]/text()')[0]
        if qty_mn == 'Backorder' or qty_wi == 'Backorder':
            if qty_wi == 'In Stock' or qty_mn == 'In Stock':
                return 100
            if len(qty_mn) > 3 and len(qty_wi) > 3:

                return('BackOrder')
        if qty_mn == 'Item not available' and qty_wi == 'Item not available':
            return('Item not available')
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



