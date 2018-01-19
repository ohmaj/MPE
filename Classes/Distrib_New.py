from abc import ABC, abstractmethod
import os
import csv
import time


class Distributor(ABC):

    def __init__(self, mfr):
        self.manufacturer = mfr
        self.root_directory = 'T:/ebay/'
        self.standardized_directory = self.root_directory + self.manufacturer + '/inventory/'
        self.product_ids_filepath = self.standardized_directory + 'ProductIds.csv'
        self.write_to_filepath = self.standardized_directory + self.manufacturer + '_Inventory_' + time.strftime(
            "%m%d%I%M") + '.csv'

    def write_inventory(self):
        inventory = self.get_inventory()
        sanitized_inventory = self.sanitize_inventory(inventory)
        self.write_dict_to_csv(sanitized_inventory)

    def get_inventory(self):
        products = self.get_product_dictionary()
        distributor_inventory = self.get_distributor_inventory_dictionary()
        updated_inventory = self.reconcile_distributor_inventory(products, distributor_inventory)
        return updated_inventory

    @staticmethod
    def reconcile_distributor_inventory(products, inventory):
        for k, v in products.items():
            try:
                v['Quantity'] = inventory[k]['Qty on Hand']

            except:
                v['Quantity'] = 'error'

        return products

    def get_product_dictionary(self):
        products = {}
        with open(self.product_ids_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                del row['Title']
                row['Fulfillment Source'] = 'Drop Shipper'
                row['Action'] = 'Reconcileto'
                row['Error'] = ''
                products[row['Product ID']] = dict(row)
            return products

    @abstractmethod
    def get_distributor_inventory_dictionary(self):
        pass

    @staticmethod
    def sanitize_inventory(inventory):
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
                          } for key, product in inventory.items()]
        return ordered_dicts

    def write_dict_to_csv(self, dictionaries):
        keys = dictionaries[0].keys()
        with open(self.write_to_filepath, 'a', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(dictionaries)

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')
