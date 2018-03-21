from lxml import html
from Classes import Distributor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import math


class AIP(Distributor.ScrapeDistributor):

    def __init__(self, manufacturer):
        super(AIP, self).__init__(manufacturer)

    def login(self, browser):
        login_url = r'https://' + self.username + ':' + self.password + '@www.aiproducts.com/dealer/customer.htm'
        browser.get(login_url)
        frame_x_path = '/html/frameset/frameset/frame[1]'
        menu_x_path = '/html/body/a[2]/p'
        sub_menu_x_path = '//*[@id="sub1"]/a[2]'
        frame = browser.find_element_by_xpath(frame_x_path)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(menu_x_path).click()
        browser.find_element_by_xpath(sub_menu_x_path).click()

    def load_product(self, product_id, browser):
        browser.switch_to.default_content()
        frame_xpath = r'/html/frameset/frameset/frame[2]'
        item_number_input_xpath = r'//html/body/form/table/tbody/tr/td[1]/table/tbody/tr[1]/td[3]/input'
        qty_input_xpath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[1]'
        check_button_xpath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[2]'
        frame = browser.find_element_by_xpath(frame_xpath)
        browser.switch_to.frame(frame)
        myElem = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, item_number_input_xpath)))
        browser.find_element_by_xpath(item_number_input_xpath).clear()
        browser.find_element_by_xpath(item_number_input_xpath).send_keys(product_id.strip('[]'))
        browser.find_element_by_xpath(qty_input_xpath).clear()
        browser.find_element_by_xpath(qty_input_xpath).send_keys('10')
        browser.find_element_by_xpath(check_button_xpath).click()

    def get_product_info(self):
        browser = self.browser
        login_url = 'https://il7660:3622elm@www.aiproducts.com/dealer/customer.htm'
        browser.get(login_url)
        with open('T:/ebay/AIP/DATA/2018/NEW_Listings.csv', encoding="utf8") as f:
            products = csv.DictReader(f)
            formatted_products = []
            for product in products:
                try:
                    scraped_product = self.load_product_details(product['Product ID'], browser)
                    formatted_product = self.format_ebay_description(scraped_product)
                    product['eBay Description'] = formatted_product['description']
                    product['Picture'] = formatted_product['images']
                    product['Product ID Type'] = 'NONE'
                    product['eBay Category1ID'] = '82248'
                    product['Primary Fulfillment Source'] = 'Self'
                    product['Secondary Fulfillment Source'] = 'Drop Shipper'
                    product['Is Taxable'] = 'True'
                    product['IS_Item Condition'] = 'New'
                    product['Title'] = 'NEW ' + product['Title'] + ' ' + product['SKU']
                    product['error'] = ''
                    formatted_products.append(product)
                except Exception as inst:
                    product['eBay Description'] = inst
                    product['Picture'] = ''
                    product['Product ID Type'] = 'NONE'
                    product['eBay Category1ID'] = '82248'
                    product['Primary Fulfillment Source'] = 'Self'
                    product['Secondary Fulfillment Source'] = 'Drop Shipper'
                    product['Is Taxable'] = 'True'
                    product['IS_Item Condition'] = 'New'
                    product['Title'] = 'NEW ' + product['Title'] + ' ' + product['SKU']
                    formatted_products.append(product)
            browser.quit()
            self.save_to_filepath = 'T:/ebay/AIP/DATA/2018/NEW_Formatted_Listings.csv'
            self.write_generic_dict_to_csv(formatted_products)

    @staticmethod
    def format_ebay_description(product):
        listing_html = ''
        listing_html = listing_html + r'<p><font color="#000000" size="4" face="Arial">' + \
            product['attributes'] + '</font></p>'
        if len(product['kit_list']) > 0:
            kit_text = ' '.join(item[0] + ': ' + item[1] + '   Qty: ' + item[2] + '<br />'
                                for item in product['kit_list'])
            listing_html = listing_html + '<p><font color="#000000" size="4" face="Arial"><b>' \
                'Kit Includes:</b><br />' + kit_text + '</font></p>'
        try:
            if len(product['crosses']) > 0:
                crosses_text = '<p><font color="#000000" size="4" face="Arial"><br /><b>' + ' '.join(sub_list[0] +
                                '</b><br />' + ' '.join([item[0] + ' ' + item[1] +
                                '<br />' if len(item) > 0 else item[0] + '<br />' for item in sub_list[1:]])for sub_list
                                in product['crosses'] if len(sub_list) > 0) + '</font></p><br />'
                listing_html = listing_html + crosses_text
        except Exception as inst:
            product['error'] = inst
        if len(product['models']) > 0:
            models_text = '<br /><p><font color="#000000" size="4" face="Arial"><b>Models:</b><br />' + \
                          '<br />'.join(product['models']) + '</font></p><br />'
            listing_html = listing_html + models_text
        product['description'] = listing_html
        return product

    def load_product_details(self, product_id, browser):
        browser.get('https://www.aiproducts.com/catalog/itemdetl.htm?ItemNumber=' + product_id.strip('[]'))
        myElem = WebDriverWait(browser, 1).\
            until(EC.presence_of_element_located((By.XPATH,
                                                  '//*[@id="LargeImg"]')))
        tree = html.fromstring(browser.page_source)
        images = 'https://www.aiproducts.com/images/' + product_id + '(1).JPG'
        attributes = ''
        crosses = []
        kit_list = []
        models = []
        if len(tree.xpath(r'//*[@id="MegaCrossArea"]/table')) > 0:
            mega_cross_trees = [tree]
            while browser.find_element_by_xpath\
                    (r'//*[@id="MegaCrossArea"]/table/tbody/tr[1]/td/table/tbody/tr/td[5]').text == 'next':
                browser.find_element_by_xpath(
                    r'//*[@id="MegaCrossArea"]/table/tbody/tr[1]/td/table/tbody/tr/td[5]/i/a').click()
                tree = html.fromstring(browser.page_source)
                mega_cross_trees.append(tree)
            crosses = self.parse_megacross(mega_cross_trees)
        if len(tree.xpath(r'//*[@id="ModelArea"]/table')) > 0:
            model_trees = [tree]
            while browser.find_element_by_xpath\
                    (r'//*[@id="ModelArea"]/table/tbody/tr[1]/td/table/tbody/tr/td[5]').text == 'next':
                browser.find_element_by_xpath(
                    r'//*[@id="ModelArea"]/table/tbody/tr[1]/td/table/tbody/tr/td[5]/i/a').click()
                tree = html.fromstring(browser.page_source)
                model_trees.append(tree)
            models = self.parse_models(model_trees)
        if len(tree.xpath(r'//*[@id="GraphicArea"]/table')) > 0:
            images = self.parse_images(tree)
        if len(tree.xpath(r'//*[@id="AttributeArea"]/table')) > 0:
            attributes = self.parse_attributes(tree)
        if len(tree.xpath(r'//*[@id="KitDetailArea"]/table')) > 0:
            kit_list = self.parse_kit_detail(tree)
        return {'Product ID': product_id,
                'images': images,
                'crosses': crosses,
                'attributes': attributes,
                'kit_list': kit_list,
                'models': models}

    @staticmethod
    def parse_images(tree):
        images = ';'.join(tree.xpath(r'//*[@id="GraphicArea"]/table/tbody/tr/td/a/img/@src'))
        return images

    @staticmethod
    def parse_attributes(tree):
        attributes = tree.xpath('//*[@id="AttributeArea"]/table/tbody/tr[1]/td/text()')[0]
        attributes = ' '.join((attributes.replace('/n', '').replace('•', '<br />').strip()).split())
        return attributes

    @staticmethod
    def parse_megacross(tree_list):
        cross_info = []
        temp_list = []
        for tree in tree_list:
            table = tree.xpath('//*[@id="MegaCrossArea"]/table')[0]
            for row in table.xpath(".//tr"):
                if len(row.xpath('.//td/b/text()')) > 0:
                    if len(temp_list) > 0:
                        del temp_list[-2:]
                        cross_info.append(temp_list)
                        temp_list = []
                    temp_list.append(row.xpath('.//td/b/text()')[0])
                if len(row.xpath('.//td[3]/a')) > 0:
                    with_link = []
                    with_link.append(row.xpath('.//td[3]/a/text()')[0])
                    if len(row.xpath('.//td[4]')[0]) > 0:
                        with_link.append([td.text for td in row.xpath('.//td[4]')][0])
                    temp_list.append(with_link)
                else:
                    temp_list.append([td.text for td in row.xpath('.//td')][2:4])
            del temp_list[-2:]
        cross_info.append(temp_list)
        del cross_info[0]
        total_length = sum(len(sub_list) for sub_list in cross_info)
        nth_quantity = int(math.ceil(total_length/60))
        if total_length > 60:
            cross_info = [sub_list[1::nth_quantity] for sub_list in cross_info]
        return cross_info

    @staticmethod
    def parse_kit_detail(tree):
        kit_info = []
        table = tree.xpath('//*[@id="KitDetailArea"]/table')[0]
        for row in table.xpath(".//tr"):
            if len(row.xpath('.//td[2]/text()')) > 0:
                product_id = row.xpath('.//td[3]/a/text()')[0]
                description = row.xpath('.//td[2]/text()')[0]
                quantity = row.xpath('.//td[5]/text()')[0].strip()
                kit_info.append([product_id, description, quantity])
        return kit_info

    @staticmethod
    def parse_models(tree_list):
        model_info = []
        for tree in tree_list:
            table = tree.xpath('//*[@id="ModelArea"]/table')[0]
            for row in table.xpath(".//tr"):
                td = [td.text for td in row.xpath('.//td[2]/a')]
                if len(td) > 0:
                    model_info.append(td[0])
        total_length = len(model_info)
        nth_quantity = int(math.ceil(total_length / 60))
        if total_length > 60:
            model_info = model_info[1::nth_quantity]
        return model_info

    def parse_scrape(self, item, html_scrape):
        tree = html.fromstring(html_scrape)
        adjust_t_r = 0
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[10]/td/img'):
            adjust_t_r = 1
        if (tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[14]/td[1]/text()')[0]) == ':':
            item['Quantity'] = 'invalid'
            return item
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[11]/td/table/tbody/tr[2]/td[2]/input'):
            item['Quantity'] = 'vendor dropship'
            return item
        ia = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 10) + ']/td[3]/text()')[0])
        ind = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                             str(adjust_t_r + 11) + ']/td[3]/text()')[0])
        mo = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 12) + ']/td[3]/text()')[0])
        nc = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 13) + ']/td[3]/text()')[0])
        tx = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 14) + ']/td[3]/text()')[0])
        ca = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 15) + ']/td[3]/text()')[0])
        wa = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 16) + ']/td[3]/text()')[0])
        pa = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 17) + ']/td[3]/text()')[0])
        ga = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 18) + ']/td[3]/text()')[0])
        fl = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 19) + ']/td[3]/text()')[0])
        qty = ia + ind + mo + nc + tx + ca + wa + pa + ga + fl
        item['Quantity'] = qty
        return item
