import csv
import os
import time
import pandas as pd
import selenium.webdriver as webdriver
from lxml import html
from Models import Data_Models


class GoldenEagle:

    def __init__(self, mfr):
        self.mfr = mfr
        self.userName = "72495"
        self.password = "3622elm"
        self.productIdsFilePath = r'T:/ebay/'+mfr+'/inventory/ProductIds.csv'
        self.resultsFilePath = r'T:/ebay/'+mfr+'/inventory/'+self.mfr+'Scrape' + time.strftime("%m%d%Y"+'.'+"%I%M") + '.csv'
        self.loginUrl = r'http://netstore.goldeneagledist.com/netstore/StartServlet'
        self.loginButtonXpath =  '//*[@id="layout-middle"]/div/div[1]/div[1]/ul/li[1]/a'
        self.usernameName = 'User'
        self.passwordName = 'Password'
        self.loginClickName = 'ACTION_SIGNON'
        self.productSearchUrl = r'http://netstore.goldeneagledist.com/netstore/ItemDetailServlet?KEY_ITEM='
        self.headerRow = ["Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action"]

    def get_update(self):
        global browser
        browser = webdriver.Chrome()
        results = self.resultsFilePath
        self.login()
        dataSet = self.getDataSet(self.productIdsFilePath)
        self.doScrape(browser, self.mfr, dataSet, results)
        browser.quit()

    def doScrape(self, browser, manufacturerCode, dataSet ,results):
        with open(results, 'a', newline='') as f:
            global writer
            writer = csv.writer(f)
            writer.writerow(self.headerRow)
            count = 1
            total = sum(1 for row in dataSet.iterrows())
            for index, row in dataSet.iterrows():
                dataFrame = Data_Models.ResultsForEbay(row)
                productID = dataFrame.productID
                self.loadProduct(manufacturerCode, productID)
                html = self.gethtml()
                if browser.title == 'Redirect':
                    while browser.title == 'Redirect':
                        browser.get(self.loginUrl)
                    self.login()
                self.saveRecord(self.parse(html, dataFrame).frameAsList)
                self.cls()
                print(self.mfr + ' Progress: '+str(int((count / total) * 100)) + '%')
                count += 1

    def getDataSet(self, fileLocation):
        ds = pd.read_csv(fileLocation, dtype=object, na_filter=False)
        return (ds)

    def login(self):
        userName = self.userName
        password = self.password
        loginUrl = self.loginUrl
        usernameName = self.usernameName
        passwordName = self.passwordName
        loginClickName = self.loginClickName
        loginButtonXpath = self.loginButtonXpath
        browser.get(loginUrl)
        browser.find_element_by_xpath(loginButtonXpath).click()
        browser.find_element_by_name(usernameName).clear()
        browser.find_element_by_name(usernameName).send_keys(userName)
        browser.find_element_by_name(passwordName).send_keys(password)
        browser.find_element_by_name(loginClickName).click()

    def loadProduct(self, manufacturerCode, partNumber):
        productSearchUrl = self.productSearchUrl
        browser.get(productSearchUrl+manufacturerCode+'++'+partNumber)


    def gethtml(self):
        return (browser.page_source)

    def parse(self, htmlScrape, data_frame):
        tree = html.fromstring(htmlScrape)
        availabilityImg = tree.xpath(
            '//*[@id="ItemDetailForm"]/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td[2]//@src')
        availability = '0'
        if len(availabilityImg) < 1:
            availability = 'Skipped'
        elif availabilityImg[0] == '/netstore/IBSStaticResources/NS_Resources/Available.gif':
            availability = '10'
        try:
            data_frame.description = tree.xpath('//*[@id="ItemThumbnails"]/div/text()')[0]

        except:
            pass
        # try:
        #     data_frame.cost = (tree.xpath('//*[@id="ItemDetailForm"]/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td[2]/table/tbody/tr[5]/td[2]/span/b[2]/span/text()')).strip(' ')
        # except:
        #     pass
        data_frame.quantity = availability
        data_frame.fulfillmentSource = "Drop Shipper"
        data_frame.getFrameAsList()
        return (data_frame)

    def saveRecord(self, dataFrame):
        writer.writerow(dataFrame)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')