from classes import ABC_Distributor
import pyodbc
import csv


class Database(ABC_Distributor.Distributor):

    def __init__(self):
        super(Database, self).__init__('All')
        self.product_ids_filepath = [r'T:/ebay/ARN/inventory/ProductIds.csv', r'T:/ebay/KAW/inventory/ProductIds.csv',
                                     r'T:/ebay/ECH/inventory/ProductIds.csv', r'T:/ebay/BIL/inventory/ProductIds.csv',
                                     r'T:/ebay/TEC/inventory/ProductIds.csv', r'T:/ebay/IC/inventory/ProductIds.csv',
                                     r'T:/ebay/HYD/inventory/ProductIds.csv', r'T:/ebay/KOH/inventory/ProductIds.csv',
                                     r'T:/ebay/MTD/inventory/ProductIds.csv', r'T:/ebay/AIP/inventory/ProductIds.csv',
                                     r'T:/ebay/STE/inventory/ProductIds.csv', r'T:/ebay/MART/inventory/ProductIds.csv',
                                     r'T:/ebay/AYP/inventory/ProductIds.csv', r'T:/ebay/FEL/inventory/ProductIds.csv',
                                     r'T:/ebay/MAR/inventory/ProductIds.csv']

    def get_product_dictionary(self):
        product_ids_dataset = list(self.get_product_ids_dataset())
        product_ids_dict = {}
        for product in product_ids_dataset:
            product['Fulfillment Source'] = 'self'
            product['Action'] = 'Reconcileto'
            product['Error'] = ''
            product_ids_dict[product['SKU']] = product
        return product_ids_dict

    def get_product_changes_dictionary(self):
        product_ids_dict = {}
        with open(r'T:/ebay/All/inventory/self_ProductIds.csv', encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                del row['Title']
                row['Fulfillment Source'] = 'self'
                row['Action'] = 'Reconcileto'
                row['Error'] = ''
                product_ids_dict[row['SKU']] = row
        return product_ids_dict

    def get_product_ids_dataset(self):
        for mfr_ids_filepath in self.product_ids_filepath:
            with open(mfr_ids_filepath, encoding="utf8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    del row['Title']
                    yield row

    def get_distributor_inventory_dictionary(self):
        connection = pyodbc.connect("DSN=Ideal ODBC")
        cursor = connection.cursor()
        cursor.execute("SELECT PRODUCT.PARTNUMBER, PRODUCT.MFRID, PRODUCTLOCATION.COMPOSITEKEY, "
                       "PRODUCT.LOOKUPPARTNUMBER, PRODUCTLOCATION.ONHANDAVAILABLEQUANTITY "
                       "FROM PRODUCTLOCATION JOIN PRODUCT ON (PRODUCTLOCATION.PARTNUMBER=PRODUCT.PARTNUMBER)")
        ideal_dataset = {}
        for row in cursor.fetchall():
            part_id = '[' + row[1] + '][' + row[0] + ']'
            ideal_dataset[part_id] = {}
            ideal_dataset[part_id]['MFRID'] = row[1]
            ideal_dataset[part_id]['COMPOSITEKEY'] = row[2]
            ideal_dataset[part_id]['SKU'] = part_id
            ideal_dataset[part_id]['LOOKUPPARTNUMBER'] = row[3]
            ideal_dataset[part_id]['Qty on Hand'] = row[4]
            ideal_dataset[part_id]['PARTNUMBER'] = row[0]
        return ideal_dataset

    @staticmethod
    def reconcile_distributor_inventory(products, inventory):
        for k, v in products.items():
            try:
                v['Quantity'] = inventory[k]['Qty on Hand']
            except:
                v['Quantity'] = 0
        return products

    def write_inventory_changes(self):
        products = self.get_product_dictionary()
        inventory = self.get_inventory()
        products_archived = self.get_product_changes_dictionary()
        inventory_changes = self.get_inventory_changes(products, inventory)
        if len(inventory_changes.items()) > 0:
            sanitized_inventory_changes = self.sanitize_inventory(inventory_changes)
            self.write_dict_to_csv(sanitized_inventory_changes)
            sanitized_inventory = self.sanitize_inventory(inventory)
            self.write_to_filepath = r'T:/ebay/All/inventory/self_ProductIds.csv'
            self.write_dict_to_new_csv(sanitized_inventory)
