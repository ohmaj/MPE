from classes import ABC_Distributor_From_File
import csv
import time


class Update_Inventory(ABC_Distributor_From_File.ABCDistributorFromFile):
    def __init__(self):
        self.ow_dump_file_path = r'T:/ebay/STE/inventory/MCHENRYPOWER.csv'
        self.currently_running_file_path = 'T:/ebay/STE/inventory/ProductIds.csv'
        self.save_to_filepath = 'T:/ebay/STE/inventory/STE_Updated_Inventory.'+time.strftime("%m%d%Y"+'.'+"%I%M")+'.csv'
        super().__init__('STE')

    def parse_file_to_dictionary(self):
        new_dict = {}
        with open(self.ow_dump_file_path) as f:
            products = [{
                'Product ID': row[0],
                'TEMPSKU': '[STE]['+row[0].replace('-', '')+']',
                'Qty on Hand': row[1],
            } for row in csv.reader(f)]
            for item in list(products):
                new_dict[item['Product ID']] = item
            return new_dict
