from Classes import ABC_Distributor_From_File
import csv


class GoldenEagleFromFile(ABC_Distributor_From_File.ABCDistributorFromFile):

    def __init__(self, mfr):
        self.distributor_inventory_filepath = 'T:/ebay/Golden Eagle/Inventory/Mchenry.csv'
        super().__init__(mfr)

    def parse_file_to_dictionary(self):
        products = {}
        with open(self.distributor_inventory_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                len_pid = len(row['Item Code'])
                item_code = row['Item Code']
                product_id = item_code[5:len_pid]
                row['Product ID'] = product_id
                row['Fulfillment Source'] = 'Drop Shipper'
                row['Action'] = 'Reconcileto'
                row['Error'] = ''
                products[row['Product ID']] = dict(row)
        return products
