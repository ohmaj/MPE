import csv
import re
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
        self.resultsFilePath = r'T:/ebay/AIP/inventory/'
        self.loginUrl = r'https://'+self.userName+':'+self.password+'@www.aiproducts.com/dealer/customer.htm'
        self.productDataSet = self.get_data_set()
        self.headerRow = ['Product ID', 'SKU', 'Product ID', 'Item ID', 'PS DESC', 'Title', 'Product Brand', 'Status', 'Product ID type', 'eBay Shipping Preset Name', 'Weight Major', 'Weight price file', 'weight minor',
                          'Dimension Length', 'Dimension Width', 'Dimension Depth', 'Is Taxable', 'Qty On Hand', 'Qty Currently Listed', 'Qty to List', 'Cost','','','dis - code', 'MSRP', 'fixed price', 'Profit', 'Fees',
                          'eBay Title', 'eBay Condition', 'eBay Description Wrapper Name', 'eBay Description', 'eBay Payment Preset Name', 'eBay Private', 'eBay Category1ID', 'eBay Store Category1Name',
                          'eBay Store Category2Name', 'eBay Allocation Plane Name', 'IS_Type', 'IS_Brand', 'IS_MPN', 'IS_Model', 'IS_UPC', 'PICTURE', 'PRE IMG']

    def get_update(self):
        global browser
        date_str = time.strftime("%m%d%Y"+'.'+"%I%M")
        results = self.resultsFilePath+'AIPInfo' + date_str + '.csv'
        browser = webdriver.Chrome()
        data_set = self.get_data_set()
        self.login()
        with open(results, 'a', newline='') as f:
            global writer
            writer = csv.writer(f)
            writer.writerow(self.headerRow)
            megacross_next_btn_xpath = r'//*[@id="MegaCrossArea"]/table/tbody/tr[1]/td/table/tbody/tr/td[5]/i/a'
            for index, row in data_set.iterrows():
                productID = (row[4]).strip('[]')
                ebay_listing = Data_Models.Ebay_Listing()
                self.loadProduct(browser, productID, 10)
                window_before = browser.window_handles[0]
                window_after = browser.window_handles[1]
                browser.switch_to.window(window_after)
                html_scrape = []
                html_scrape.append(browser.page_source)
                try:
                    nextButton = browser.find_element_by_xpath(megacross_next_btn_xpath).text
                    while nextButton == 'next':
                        try:
                            browser.find_element_by_xpath(megacross_next_btn_xpath).click()
                            browser.find_element_by_xpath(megacross_next_btn_xpath).click()
                            time.sleep(.1)
                            html_scrape.append(browser.page_source)
                        except:
                            nextButton = ''
                            pass
                except:
                    pass
                browser.close()
                browser.switch_to.window(window_before)
                aip_scrape = self.parse(html_scrape)
                aip_scrape.get_list()
                ebay_listing.product_id1 = productID
                ebay_listing.product_id2 = '['+productID+']'
                ebay_listing.sku = '[AIP]['+productID+']'
                # ebay_listing.ps_desc =
                # ebay_listing.title =
                ebay_listing.product_brand = 'AIP'
                ebay_listing.qty_on_hand = 1000
                ebay_listing.weight_price_file = re.sub(r'([^0-9,/.])+', '', aip_scrape.list[2])
                ebay_listing.qty_currently_listed = 0
                ebay_listing.qty_to_List = 3
                # ebay_listing.eBay_title =
                ebay_listing.status = 'UnderConstruction'
                ebay_listing.dis_code =  'A'
                ebay_listing.eBay_condition = 'NEW'
                ebay_listing.eBay_private = 'TRUE'
                ebay_listing.eBay_category1ID =  82248
                ebay_listing.eBay_store_category1_name = 'Brand Parts'
                ebay_listing.eBay_allocation_plane_name = 'keep 3 listed'
                ebay_listing.is_brand = 'A&I'
                ebay_listing.is_model = 0
                ebay_listing.is_upc = ''
                ebay_listing.pre_img = 0
                # ebay_listing.ps_desc = aip_scrape.list[1]
                ebay_listing.picture = aip_scrape.list[0]
                ebay_listing.eBay_description = aip_scrape.list[1]
                ebay_listing.is_mpn = ebay_listing.sku
                ebay_listing.get_list()
                self.saveRecord(ebay_listing.as_list)
        browser.quit()

    def get_data_set(self):
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
        moreInfoLinkXPath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[1]/td[3]/a/img'
        frame = browser.find_element_by_xpath(frameXPath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(itemNumberInputXPath).clear()
        browser.find_element_by_xpath(itemNumberInputXPath).send_keys(partNumber)
        browser.find_element_by_xpath(qtyInputXPath).clear()
        browser.find_element_by_xpath(qtyInputXPath).send_keys(qty)
        browser.find_element_by_xpath(checkButtonXPath).click()
        browser.find_element_by_xpath(moreInfoLinkXPath).click()

    def getAtttributeData(self, table):
        tbody = table[0]
        listOfAttributes = []
        for tr in tbody:
            kvp = []
            for td in tr:
                cellString = str(' '.join(str(td.text).split())).replace('None','')
                if cellString:
                    kvp.append(cellString)
                for b in td:
                    kvp.append(b.text)
            if len(kvp) > 0:
                listOfAttributes.append(' '.join(kvp))
        if len(listOfAttributes) >0:
            return (listOfAttributes)

    def getImgData(self, table):
        list_img_links = []
        try:
            tbody = table[0]
            for tr in tbody:
                for td in tr:
                    for a in td:
                        for img in a:
                            list_img_links.append(img.get("src"))
        except:
            pass
        return list_img_links[0]

    def getMegaCrossData(self, table):
        tbody = table[0]
        listOfMegaCross = []
        kvp = []
        key = None
        for tr in tbody:
            partMfrKvp = []
            for td in tr:
                cellString = str(' '.join(str(td.text).split())).replace('None','')
                if cellString:
                    partMfrKvp.append(cellString)
                for element in td:
                    cellString = str(' '.join(str(element.text).split())).replace('None', '')
                    if cellString:
                        if element.get('href'):
                            partMfrKvp.append(cellString)
                        else:
                            if key :
                                listOfMegaCross.append([key,kvp])
                                kvp = []
                            key = cellString
            if len(partMfrKvp) > 1:
                kvp.append(' '.join(partMfrKvp))
        listOfMegaCross.append([key, kvp])
        return(listOfMegaCross)

    def getKitDetailData(self, table):
        tbody = table[0]
        list_kit_detail = []
        kvp = []
        key = None
        row_index = 1
        for tr in tbody:
            part_info = []
            cell_index = 1
            if row_index > 2:
                for td in tr:
                    cellString = str(' '.join(str(td.text).split())).replace('None','')
                    if cellString:
                        if cell_index == 2:
                            if key != None:
                                list_kit_detail.append([key,kvp])
                                kvp = []
                            key = cellString
                        elif len(cellString) > 0:
                            part_info.append(cellString)
                    for element in td:
                        elementString = str(' '.join(str(element.text).split())).replace('None', '')
                        if elementString:
                            if element.get('href'):
                                part_info.append(elementString)
                    cell_index += 1
            row_index += 1
            if len(part_info) > 1:
                kvp.append(' '.join(part_info))
        list_kit_detail.append([key, kvp])
        return (list_kit_detail)

    def getKitMasterData(self, table):
        tbody = table[0]
        list_kit_master = []
        kvp = []
        row_index = 1
        for tr in tbody:
            part_info = []
            if row_index > 2:
                for td in tr:
                    cellString = str(' '.join(str(td.text).split())).replace('None','')
                    if cellString:
                        part_info.append(cellString)
                    for element in td:
                        elementString = str(' '.join(str(element.text).split())).replace('None', '')
                        if elementString:
                            if element.get('href'):
                                part_info.append(elementString)
            row_index += 1
            if len(part_info) > 1:
                kvp.append(' '.join(part_info))
        list_kit_master.append(kvp)
        return (list_kit_master)

    def get_model_data(self, table):
        tbody = table[0]
        list_models = []
        row_index = 1
        for tr in tbody:
            if row_index > 2:
                for td in tr:
                    for element in td:
                        elementString = str(' '.join(str(element.text).split())).replace('None', '')
                        if elementString:
                            if element.get('href'):
                                list_models.append(elementString)
            row_index += 1
        return (list_models)

    def parse(self, htmlScrape):
        list_of_scrapes = htmlScrape
        tree = html.fromstring(list_of_scrapes[0])
        graphicArea = tree.xpath(r'//*[@id="GraphicArea"]/table/tbody')
        attributeArea = tree.xpath(r'//*[@id="AttributeArea"]/table/tbody')
        # megaCrossArea = tree.xpath(r'//*[@id="MegaCrossArea"]/table/tbody')
        # kitDetailArea = tree.xpath(r'//*[@id="KitDetailArea"]/table/tbody')
        # kitMasterArea = tree.xpath(r'//*[@id="KitMasterArea"]/table/tbody')
        modelArea = tree.xpath(r'//*[@id="ModelArea"]/table/tbody')
        weight = tree.xpath(r'/html/body/table/tbody/tr[4]/td[1]/table[1]/tbody/tr[3]/td[3]')
        aip_scrape = Data_Models.AIP_Scrape()
        try:
            aip_scrape.weight  = weight[0].text
        except:
            pass
        # --------- other areas not being used at this time ----------------------
        # externalPageArea = tree.xpath(r'//*[@id="ExternalPageArea"]/table/tbody')
        # componentArea = tree.xpath(r'//*[@id="ComponentArea"]/table/tbody')
        # associateArea = tree.xpath(r'//*[@id="AssociateArea"]/table/tbody')
        # alternateArea = tree.xpath(r'//*[@id="AlternateArea"]/table/tbody')
        # comparableArea = tree.xpath(r'//*[@id="ComparableArea"]/table/tbody')
        # manualArea = tree.xpath(r'//*[@id="ManualArea"]/table/tbody')
        if len(attributeArea) > 0:
            aip_scrape.product_attributes = self.getAtttributeData(attributeArea)
        if len(graphicArea) > 0:
            aip_scrape.graphics = self.getImgData(graphicArea)
        # if len(list_of_scrapes)> 1:
        #     for scrape in list_of_scrapes:
        #         tree_additional = html.fromstring(scrape)
        #         megaCrossArea_additional = tree_additional.xpath(r'//*[@id="MegaCrossArea"]/table/tbody')
        #         aip_scrape.megaCross = self.getMegaCrossData(megaCrossArea_additional)
        # elif len(megaCrossArea) > 0:
        #     aip_scrape.megaCross = self.getMegaCrossData(megaCrossArea)
        # if len(kitDetailArea) > 0:
        #     aip_scrape.kitDetails = self.getKitDetailData(kitDetailArea)
        # if len(kitMasterArea) > 0:
        #     aip_scrape.kitMaster = self.getKitMasterData(kitMasterArea)
        if len(modelArea) > 0:
            aip_scrape.models = self.get_model_data(modelArea)
        return aip_scrape

    def saveRecord(self, dataFrame):
        try:
            writer.writerow(dataFrame)
        except:
            pass
