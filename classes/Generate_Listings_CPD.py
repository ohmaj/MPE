from models import Listing_Model
from classes import Parts_Tree_Scraper
import csv
import time
import os


class Ebay:

    def __init__(self):
        self.mfr_code = 'KOH'
        self.mfr_name = 'kohler-engines'
        self.product_ids_filepath = r'T:/ebay/' + self.mfr_code + '/Data/2018/ProductIds.csv'
        self.save_to_filepath = r'T:/ebay/' + self.mfr_code + '/Data/2018/Generated_Listings' \
                                + time.strftime("%m%Y") + '.csv'

    def write_listing(self):
        products = list(self.get_new_products())
        products = list(self.set_partstree_info(products))
        products_s = list(self.set_partstree_info(products))
        products = products + products_s
        self.write_to_file(products)

    def get_new_products(self):
        print("Getting Product Ids...")
        with open(self.product_ids_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield (row)

    def set_partstree_info(self, products):
        parts_tree_scraper = Parts_Tree_Scraper.PartsTreeScraper(self.mfr_code, self.mfr_name)
        count = 1
        total = len(products)
        for product in products:
            parts_tree_part = parts_tree_scraper.get_scrape_single(product['Product ID'])
            product['Picture'] = parts_tree_part.part_thumbnail_src
            product['Where Used'] = parts_tree_part.compatable_machines
            self.cls()
            print('Getting Parts Tree Info: ' + str(int((count / total) * 100)) + '%')
            count += 1
            yield (product)
        print('testing')

    def set_partstree_info_s(self, products):
        parts_tree_scraper = Parts_Tree_Scraper.PartsTreeScraper(self.mfr_code, self.mfr_name)
        count = 1
        total = len(products)
        for product in products:
            parts_tree_part = parts_tree_scraper.get_scrape_single(product['Product ID'] + '-s')
            product['Picture'] = parts_tree_part.part_thumbnail_src
            product['Where Used'] = parts_tree_part.compatable_machines
            self.cls()
            print('Getting Parts Tree Info: ' + str(int((count / total) * 100)) + '%')
            count += 1
            yield (product)
        print('testing')

    def write_to_file(self, products):
        print('Writing File....')
        listings = list(self.get_listing_model(products))
        keys = listings[0].keys()
        with open(self.save_to_filepath, 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(listings)

    def get_listing_model(self, products):
        print('Creating Listings...')
        for product in products:
            listing = Listing_Model.CreateEbayListing()
            listing.product_id = product['Product ID']
            listing.product_mfr = self.mfr_code
            listing.product_brand = self.mfr_name
            listing.raw_title = product['Title']
            listing.where_used = product['Where Used']
            listing.msrp = product['MSRP']
            listing.weight_pricefile = product['Weight']
            listing.cost = product['Cost']
            listing.picture_url = product['Picture']
            listing.is_brand = self.mfr_name
            listing.set_all()
            yield (listing.get_part_as_dict())

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')


generate = Ebay()
generate.write_listing()
