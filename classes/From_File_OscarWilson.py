from classes import ABC_Distributor_From_File
import csv


class UpdateInventory(ABC_Distributor_From_File.ABCDistributorFromFile):
    def __init__(self, mfr):
        self.distributor_inventory_filepath = r'T:/ebay/Oscar_Wilson/McHenryDumpFile.csv'
        super().__init__(mfr)

    def parse_file_to_dictionary(self):
        ow_dict = {}
        with open(self.distributor_inventory_filepath) as f:
            ow_products = [{
                'OW Vendor Code': row[0],
                'Manufacturer Item No': row[1],
                'OW Item Number': row[2],
                'TEMPSKU': '['+row[0]+']['+row[1]+']',
                'Description': row[3],
                'Cost': row[4],
                'MSRP': row[5],
                'Qty on Hand': row[6],
                'Sub To Manufacturer Item number': row[7],
                'Sub To Vendor Code': row[8],
                'Status': row[9],
                'Manufacturer Code': row[10],
                'Manufacturer': row[11],
                'OW Sub Number': row[12],
            } for row in csv.reader(f)]
            for item in list(ow_products):
                key = item['Manufacturer Item No']
                ow_dict[key] = item
            return ow_dict
