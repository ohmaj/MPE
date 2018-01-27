from classes import User_Info
from classes import ABC_Distributor
from abc import abstractmethod
import csv
import selenium.webdriver as webdriver


class DistributorScrape(ABC_Distributor.Distributor):

    def __init__(self, mfr):
        self.username = None
        self.password = None
        self.browser = None
        super().__init__(mfr)

    def set_credentials(self):
        try:
            credentials = User_Info.Credentials(self.manufacturer)
            credentials.get_account_credentials()
            credentials.set_logon_info()
            self.username = credentials.username
            self.password = credentials.password
        except:
            print("error getting Credentials")

    def get_product_list(self):
        with open(self.product_ids_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                del row['Title']
                row['Error'] = ''
                yield (row)

    def get_distributor_inventory_dictionary(self):
        self.browser = webdriver.Firefox()
        self.set_credentials()
        self.login()
        products = list(self.get_product_list())
        count = 1
        total = len(products)
        distributor_inventory = {}
        for item in products:
            if count % 600 == 0:
                self.browser.quit()
                self.browser = webdriver.Firefox()
                self.login()
            try:
                # goto part page
                self.load_product(item['Product ID'], self.browser)
                # scrape part page
                scrape = self.browser.page_source
                # parse scrape
                updated_part = self.parse_scrape(item, scrape)
                # return parse
                self.cls()
                print('Scrape Progress: ' + str(int((count / total) * 100)) + '%')
                count += 1
                distributor_inventory[updated_part['Product ID']] = updated_part
            except Exception as inst:
                item['Quantity'] = 'Error'
                item['Error'] = inst.__str__()
                try:
                    self.login()
                except:
                    try:
                        self.browser.close()
                    except:
                        pass
                    self.browser = webdriver.Firefox()
                    self.login()
                    distributor_inventory[item['Product ID']] = item
        self.browser.quit()
        return distributor_inventory

    @abstractmethod
    def load_product(self, product_id, browser):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def parse_scrape(self, item, scrape):
        pass
