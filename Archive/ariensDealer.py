import csv
import os
import re
import time

import pandas as pd
import selenium.webdriver as webdriver
from lxml import html

from Models import Data_Models


class Ariens:

    def __init__(self):
        self.userName = "78919678"
        self.password = "3622ELMSTR"
        self.productIdsFilePath = r'T:/ebay/ARN/inventory/ProductIds.csv'
        self.resultsFilePath = r'T:/ebay/ARN/inventory/AriensScrape' + time.strftime("%m%d%Y"+'.'+"%I%M") + '.csv'
        self.loginUrl = "http://connect.ariens.com/cgibin/pnrg0099d"
        self.userNameXPath = r'//*[@id="body"]/form/table/tbody/tr[2]/td/input'
        self.passwordXPath = r'//*[@id="body"]/form/table/tbody/tr[4]/td/input'
        self.loginClickXPath = r'//*[@id="body"]/form/table/tbody/tr[8]/td[2]/input[1]'
        self.productSearchUrl = r'http://connect.ariens.com/cgibin/pnrg0099f?dmcust=78919678Browser=NetscapeVersion=5.0%20Screen=1920x1080Level=AG011000000Program=/cgibin/gprg0248'
        self.productDataSet = self.getDataSet()
        self.headerRow = ["Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action"]

    def get_update(self):
        global browser
        browser = webdriver.Chrome()
        dataSet = self.getDataSet()
        self.login()
        refreshCounter = 0
        with open(self.resultsFilePath, 'a', newline='') as f:
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
                productID = (dataFrame.productID).strip("[]")
                self.loadProduct(productID, 100)
                html = self.gethtml()
                availQty = self.parse(html)
                dataFrame.quantity = availQty
                dataFrame.fulfillmentSource = "Drop Shipper"
                dataFrame.getFrameAsList()
                self.saveRecord(dataFrame.frameAsList)
                refreshCounter += 1
                self.cls()
                print('Ariens Progress: '+str(int((count / total) * 100)) + '%')
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
        browser.find_element_by_xpath(userNameXpath).send_keys(userName)
        browser.find_element_by_xpath(passwordXpath).send_keys(password)
        browser.find_element_by_xpath(loginClickXPath).click()

    def loadProduct(self, partNumber, qty):
        productSearchUrl = self.productSearchUrl
        partNumberXPath = '/html/body/form/table[2]/tbody/tr[1]/td[3]/input'
        qtyXPath = '/html/body/form/table[2]/tbody/tr[3]/td[3]/input'
        submitButtonXPath = r'/html/body/form/center/input[2]'
        frameXPath = r'/html/frameset/frame[2]'
        browser.get(productSearchUrl)
        frame = browser.find_element_by_xpath(frameXPath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(partNumberXPath).send_keys(partNumber)
        browser.find_element_by_xpath(qtyXPath).send_keys(qty)
        browser.find_element_by_xpath(submitButtonXPath).click()

    def gethtml(self):
        return (browser.page_source)

    def parse(self, htmlScrape):
        tree = html.fromstring(htmlScrape)
        qty = tree.xpath('/html/body/table[2]/tbody/tr[2]/td[4]/text()')
        if len(qty) < 1:
            return ('invalid part number')
        else:
            qty = re.sub('[^0-9]','',qty[0])
            return (qty)

    def saveRecord(self, dataFrame):
        writer.writerow(dataFrame)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')



