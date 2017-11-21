import csv
import time


class Update_Inventory:
    def __init__(self, mfr):
        self.mfr = mfr
        self.ow_dump_file_path = r'T:/ebay/Oscar_Wilson/McHenryDumpFile.csv'
        self.currently_running_file_path = 'T:/ebay/'+mfr+'/inventory/ProductIds.csv'
        self.save_to_filepath = 'T:/ebay/'+mfr+'/inventory/'+mfr+'_Updated_Inventory.'+time.strftime("%m%d%Y"+'.'+"%I%M")+'.csv'

    def write_inventory(self):
        data_set_from_ow = self.read_from_ow()
        data_set_running_listings = self.read_current_running()
        joined_data_set = list(self.join_on_key(data_set_from_ow, data_set_running_listings))
        self.write_new_inventory(joined_data_set)


    def read_from_ow(self):
        ow_dict = {}
        with open(self.ow_dump_file_path) as f:
            ow_products = [{
                'OW Vendor Code': row[0],
                'Manufacturer Item No': row[1],
                'OW Item Number': row[2],
                'TEMPSKU': '['+row[0]+']['+row[1]+']',
                'Description': row[3],
                'Cost': row[4],
                'MSRP': row[5],
                'Qty Available': row[6],
                'Sub To Manufacturer Item number': row[7],
                'Sub To Vendor Code': row[8],
                'Status': row[9],
                'Manufacturer Code': row[10],
                'Manufacturer': row[11],
                'OW Sub Number': row[12],
            } for row in csv.reader(f)]
            for item in list(ow_products):
                ow_dict[item['TEMPSKU']] = item
            return ow_dict

    def read_current_running(self):
        running_dict = {}
        with open(self.currently_running_file_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                del row['Title']
                row['Fulfillment Source'] = 'Drop Shipper'
                row['Action'] = 'Reconcileto'
                row['TEMPSKU'] = '[' + self.mfr + '][' + row['Product ID'] + ']'
                if self.mfr == 'AYP':
                    row['TEMPSKU'] = '[HOP][' + row['Product ID'] + ']'
                running_dict[row['TEMPSKU']] = row
        return (running_dict)

    def join_on_key(self, ow, running):
        for part, info in running.items():
            try:
                matched_ow_part = ow[info['TEMPSKU']]
                info['Status'] = matched_ow_part['Status']
                info['Sub To Manufacturer Item number'] = matched_ow_part['Sub To Manufacturer Item number']
                info['Sub To Vendor Code'] = matched_ow_part['Sub To Vendor Code']
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