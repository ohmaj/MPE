import csv
import os
import time

import pandas as pd
import selenium.webdriver as webdriver
from lxml import html

from Models import Data_Models


class Kawasaki:

    def __init__(self):
        # self.userName = "51948"
        # self.password = "51948"
        self.productIdsFilePath = r'T:/ebay/KAW/inventory/ProductIds.csv'
        self.resultsFilePath = r'T:/ebay/KAW/inventory/KAW_Scrape' + time.strftime("%m%d%Y"+'.'+"%I%M") + '.csv'
        # self.loginUrl = 'https://www.kawasakipower.com/Kawasaki/login.jsp'
        # self.usernameName = 'usercode'
        # self.passwordName = 'password'
        # self.loginClickName = 'Login'
        self.productSearchUrl = 'https://kawasakipower.com/ProductDetail?DealerID=51948&UserID=kmc51948&SessionID=550577559254125&ProductID='
        self.productDataSet = self.getDataSet()
        self.headerRow = ["Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action"]

    def get_update(self):
        global browser
        results = self.resultsFilePath
        browser = webdriver.Chrome()
        dataSet = self.getDataSet()
        refreshCounter = 0
        with open(results, 'a', newline='') as f:
            global writer
            writer = csv.writer(f)
            writer.writerow(self.headerRow)
            count = 1
            total = sum(1 for row in dataSet.iterrows())
            for index, row in dataSet.iterrows():
                if refreshCounter >= 100:
                    browser.quit()
                    browser = webdriver.Chrome()
                    refreshCounter = 0
                dataFrame = Data_Models.ResultsForEbay(row)
                productID = dataFrame.productID
                self.loadProduct(productID)
                html = self.gethtml()
                availQty = self.parse(html)
                dataFrame.quantity = availQty
                dataFrame.fulfillmentSource = "Drop Shipper"
                dataFrame.getFrameAsList()
                self.saveRecord(dataFrame.frameAsList)
                refreshCounter += 1
                self.cls()
                print('Kawasaki Progress: '+str(int((count / total) * 100)) + '%')
                count += 1
        browser.quit()

    def getDataSet(self):
        ds = pd.read_csv(self.productIdsFilePath, dtype=object, na_filter=False)
        return (ds)

    # def login(self):
    #     userName = self.userName
    #     password = self.password
    #     loginUrl = self.loginUrl
    #     usernameName = self.usernameName
    #     passwordName = self.passwordName
    #     loginClickName = self.loginClickName
    #     browser.get(loginUrl)
    #     browser.find_element_by_name(usernameName).send_keys(userName)
    #     browser.find_element_by_name(passwordName).send_keys(password)
    #     browser.find_element_by_name(loginClickName).click()

    def loadProduct(self, partNumber):
        productSearchUrl = self.productSearchUrl
        browser.get(productSearchUrl+partNumber+'&ProductQlfr=KWE')

    def gethtml(self):
        return (browser.page_source)

    def parse(self, htmlScrape):
        tree = html.fromstring(htmlScrape)
        availability_imgs = tree.xpath('//*[@id="product-detail"]//img/@src')
        availability = '0'
        if len(availability_imgs) > 0:
            for src in availability_imgs:
                if src == '/img/legend/diamond-green-1.gif':
                    availability = '10'
                    break
        return (availability)

    def saveRecord(self, dataFrame):
        writer.writerow(dataFrame)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')