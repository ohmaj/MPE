from Classes import User_Info
import time
import csv
import os
import selenium.webdriver as webdriver
from random import randint


class ScrapeDistributor(object):

    def __init__(self, manufacturer):
        self.manufacturer = manufacturer
        self.username = None
        self.password = None
        self.product_source_filepath = r'T:/ebay/' + self.manufacturer + '/inventory/ProductIds.csv'
        self.save_to_filepath = r'T:/ebay/' + self.manufacturer + '/inventory/' + self.manufacturer + 'Scrape' + \
                                time.strftime("%m%d%Y" + '.' + "%I%M") + '.csv'
        self.browser = webdriver.Firefox()

    def write_inventory(self):
        self.set_credentials()
        self.login(self.browser)
        # get data set
        products = list(self.get_product_list())
        # iterate through data set
        updated_products = list(self.get_distributor_inventory(products))
        self.write_dict_to_csv(updated_products)
        try:
            self.browser.quit()
        except:
            pass

    def write_inventory_threaded(self, number_batches, number_batch):
        self.set_credentials()
        self.login(self.browser)
        # get data set
        products = list(self.get_product_list())
        total = len(products)
        number_batches = number_batches
        number_batch = number_batch
        size_batch = total/number_batches
        start_index = (total/number_batches)*number_batch
        end_index = start_index+size_batch-1
        if end_index > total-1:
            end_index = total-1
        products = products[int(start_index):int(end_index)]
        # iterate through data set
        updated_products = list(self.get_distributor_inventory(products))
        self.write_dict_to_csv(updated_products)
        try:
            self.browser.quit()
        except:
            pass

    def get_inventory(self):
        self.set_credentials()
        self.login(self.browser)
        # get data set
        products = list(self.get_product_list())
        # iterate through data set
        updated_products = list(self.get_distributor_inventory(products))
        try:
            self.browser.close()
        except:
            pass
        return updated_products

    def set_credentials(self):
        try:
            credentials = User_Info.Credentials(self.manufacturer)
            credentials.get_account_credentials()
            credentials.set_logon_info()
            self.username = credentials.username
            self.password = credentials.password
        except:
            print("error getting Credentials")

    def login(self, browser):
        pass

    def get_product_list(self):
        with open(self.product_source_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                del row['Title']
                row['Fulfillment Source'] = 'Drop Shipper'
                row['Action'] = 'Reconcileto'
                row['Error'] = ''
                yield (row)

    def get_distributor_inventory(self, products):
        count = 1
        total = len(products)
        random_int = randint(0, 9)*(randint(0, 9)+50)
        for item in products:
            if count % 500 + random_int == 0:
                self.browser.quit()
                self.browser = webdriver.Firefox()
                self.login(self.browser)
            try:
                # goto part page
                self.load_product(item['Product ID'], self.browser)
                # scrape part page
                scrape = self.scrape_page(self.browser)
                # parse scrape
                updated_part = self.parse_scrape(item, scrape)
                # return parse
                self.cls()
                print('Scrape Progress: ' + str(int((count / total) * 100)) + '%')
                count += 1
                yield(updated_part)
            except Exception as inst:
                item['Quantity'] = 'Error'
                item['Error'] = inst.__str__()
                try:
                    self.login(self.browser)
                except:
                    try:
                        self.browser.close()
                    except:
                        pass
                    self.browser = webdriver.Firefox()
                    self.login(self.browser)
                yield (item)

    def load_product(self, product_id, browser):
        pass

    @staticmethod
    def scrape_page(browser):
        return browser.page_source

    def parse_scrape(self, item, scrape):
        pass

    def write_dict_to_csv(self, updated_products):
        ordered_dicts = [{'Item ID': product['Item ID'],
                          'External Item ID': product['External Item ID'],
                          'SKU': product['SKU'],
                          'Product ID': product['Product ID'],
                          'Storage Location': product['Storage Location'],
                          'Quantity': product['Quantity'],
                          'Cost': product['Cost'],
                          'Supplier ID': product['Supplier ID'],
                          'Supplier Account Num': product['Supplier Account Num'],
                          'Supplier Name': product['Supplier Name'],
                          'Date Purchased': product['Date Purchased'],
                          'Fulfillment Source': 'Drop Shipper',
                          'PO Number': product['PO Number'],
                          'Invoice Number': product['Invoice Number'],
                          'Action': 'Reconcileto',
                          'Error': product['Error']
                          } for product in updated_products]
        print('Writing File....')
        keys = ordered_dicts[0].keys()
        with open(self.save_to_filepath, 'a', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(ordered_dicts)

    def write_generic_dict_to_csv(self, updated_products):
        print('Writing File....')
        keys = updated_products[0].keys()
        with open(self.save_to_filepath, 'a', newline='', encoding='utf-8') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(updated_products)

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')
