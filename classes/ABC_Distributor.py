from abc import ABC, abstractmethod
import os
import csv
import time


class Distributor(ABC):

    def __init__(self, mfr):
        self.header = True
        self.manufacturer = mfr
        self.root_directory = 'T:/ebay/'
        self.standardized_directory = self.root_directory + self.manufacturer + '/inventory/'
        self.product_ids_filepath = self.standardized_directory + 'ProductIds.csv'
        self.write_to_filepath = self.standardized_directory + self.manufacturer + '_Inventory_' + time.strftime(
            "%m%d%I%M") + '.csv'

    def write_inventory_changes(self):
        products = self.get_product_dictionary()
        inventory = self.get_inventory()
        inventory_changes = self.get_inventory_changes(products, inventory)
        if len(inventory_changes.items()) > 0:
            sanitized_inventory_changes = self.sanitize_inventory(inventory_changes)
            self.write_dict_to_csv(sanitized_inventory_changes)
            sanitized_inventory = self.sanitize_inventory(inventory)
            self.write_to_filepath = self.product_ids_filepath
            self.write_dict_to_new_csv(sanitized_inventory)

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
    def get_inventory_changes(old_inventory, new_inventory):
        changes_inventory = {}
        for k, v in new_inventory.items():
            try:
                if int(v['Quantity']) != int(old_inventory[k]['Quantity']):
                    changes_inventory[k] = v
            except:
                pass
        return changes_inventory

    @staticmethod
    def reconcile_distributor_inventory(products, inventory):
        for k, v in products.items():
            try:
                v['Quantity'] = inventory[k.strip('[]')]['Qty on Hand']
            except:
                v['Quantity'] = 'Error'
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
                          'Title': '',
                          'Error': product['Error']
                          } for key, product in inventory.items()]
        return ordered_dicts

    def write_dict_to_csv(self, dictionaries):
        keys = dictionaries[0].keys()
        with open(self.write_to_filepath, 'a', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            if self.header is True:
                dict_writer.writeheader()
            dict_writer.writerows(dictionaries)

    def write_dict_to_new_csv(self, dictionaries):
        keys = dictionaries[0].keys()
        with open(self.write_to_filepath, 'w', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(dictionaries)

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    @abstractmethod
    def get_distributor_inventory_dictionary(self):
        pass
