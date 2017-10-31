import pyodbc
import csv
import time

class database_connection():
    def __init__(self):
        self.product_ids_filepaths = [r'T:/ebay/ARN/inventory/ProductIds.csv',r'T:/ebay/KAW/inventory/ProductIds.csv',r'T:/ebay/ECH/inventory/ProductIds.csv',r'T:/ebay/BIL/inventory/ProductIds.csv',
                                      r'T:/ebay/TEC/inventory/ProductIds.csv',r'T:/ebay/IC/inventory/ProductIds.csv',r'T:/ebay/HYD/inventory/ProductIds.csv',r'T:/ebay/KOH/inventory/ProductIds.csv',
                                      r'T:/ebay/MTD/inventory/ProductIds.csv',r'T:/ebay/AIP/inventory/ProductIds.csv',r'T:/ebay/STE/inventory/ProductIds.csv']
        self.save_to_filepath = r'T:/ebay/All/inventory/'+ 'Self_Scrape' + time.strftime("%m%d%Y" + '.' + "%I%M") + '.csv'

    def main(self):
        product_ids_dataset = list(self.get_product_ids_dataset())
        ideal_dataset = self.get_ideal_dataseet()
        for product in product_ids_dataset:
            product['Fulfillment Source'] = 'self'
            product['Action'] = 'Reconcileto'
            try:
                sku = product['SKU'].replace(' ', '').replace('-', '')
                try:
                    product['Quantity'] = ideal_dataset[sku]['ONHANDAVAILABLEQUANTITY']
                except:
                    product['Quantity'] = 0
            except:
                product['Quantity'] = 'error'
        self.write_dict_to_csv(product_ids_dataset)

    def get_product_ids_dataset(self):
        for mfr_ids_filepath in self.product_ids_filepaths:
            with open(mfr_ids_filepath, encoding="utf8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    del row['Title']
                    yield (row)

    def get_ideal_dataseet(self):
        connection = pyodbc.connect("DSN=Ideal ODBC")
        cursor = connection.cursor()
        # for row in cursor.tables():
        #     print (row.table_name)
        # for row in cursor.columns(table='PRODUCT'):
        #     print (row.column_name)
        cursor.execute("SELECT PRODUCT.PARTNUMBER, PRODUCT.MFRID, PRODUCTLOCATION.COMPOSITEKEY, "
                       "PRODUCT.LOOKUPPARTNUMBER, PRODUCTLOCATION.ONHANDAVAILABLEQUANTITY "
                       "FROM PRODUCTLOCATION JOIN PRODUCT ON (PRODUCTLOCATION.PARTNUMBER=PRODUCT.PARTNUMBER)")
        ideal_dataset = {}
        for row in cursor.fetchall():
            sku = '['+row[1]+']['+row[3]+']'
            ideal_dataset[sku] = {}
            ideal_dataset[sku]['MFRID'] = row[1]
            ideal_dataset[sku]['COMPOSITEKEY'] = row[2]
            ideal_dataset[sku]['SKU'] = '[' + row[1] + '][' + row[2] + ']'
            ideal_dataset[sku]['LOOKUPPARTNUMBER'] = row[3]
            ideal_dataset[sku]['ONHANDAVAILABLEQUANTITY'] = row[4]
            ideal_dataset[sku]['PARTNUMBER'] = row[0]
        return (ideal_dataset)

    def write_dict_to_csv(self, updated_products):
        print('Writing File....')
        keys = updated_products[0].keys()
        with open(self.save_to_filepath, 'a', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(updated_products)