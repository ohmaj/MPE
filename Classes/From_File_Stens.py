import csv
import time


class Update_Inventory:
    def __init__(self):
        self.ow_dump_file_path = r'T:/ebay/STE/inventory/MCHENRYPOWER.csv'
        self.currently_running_file_path = 'T:/ebay/STE/inventory/ProductIds.csv'
        self.save_to_filepath = 'T:/ebay/STE/inventory/STE_Updated_Inventory.'+time.strftime("%m%d%Y"+'.'+"%I%M")+'.csv'

    def get_update(self):
        data_set_from_ow = self.read_from_ste()
        data_set_running_listings = self.read_current_running()
        joined_data_set = list(self.join_on_key(data_set_from_ow, data_set_running_listings))
        self.write_new_inventory(joined_data_set)


    def read_from_ste(self):
        dict = {}
        with open(self.ow_dump_file_path) as f:
            products = [{
                'Product ID': row[0],
                'TEMPSKU': '[STE]['+row[0].replace('-','')+']',
                'Qty Available': row[1],
            } for row in csv.reader(f)]
            for item in list(products):
                print(item['TEMPSKU'])
                dict[item['TEMPSKU']] = item
            return dict

    def read_current_running(self):
        running_dict = {}
        with open(self.currently_running_file_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                del row['Title']
                row['Fulfillment Source'] = 'Drop Shipper'
                row['Action'] = 'Reconcileto'
                row['TEMPSKU'] = '[STE][' + row['Product ID'].replace('-','') + ']'
                running_dict[row['TEMPSKU']] = row
        return (running_dict)

    def join_on_key(self, ow, running):
        for part, info in running.items():
            try:
                matched_ow_part = ow[info['TEMPSKU']]
                info['Quantity'] = matched_ow_part['Qty Available']
                yield (info)
            except:
                info['Quantity'] = 'Error'
                yield (info)

    def get_output_data_set(self, input_data_set):

        output = None
        return output

    def write_new_inventory(self, updated_products):
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
                          'Fulfillment Source': product['Fulfillment Source'],
                          'PO Number': product['PO Number'],
                          'Invoice Number': product['Invoice Number'],
                          'Action': product['Action']
                          } for product in updated_products]
        keys = ordered_dicts[0].keys()
        with open(self.save_to_filepath, 'a', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(ordered_dicts)