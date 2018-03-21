from Classes import ABC_Distributor_From_File
import csv
import xlrd


class GoldenEagleFromFile(ABC_Distributor_From_File.ABCDistributorFromFile):

    def __init__(self, mfr):
        self.distributor_inventory_filepath = 'T:/ebay/Golden Eagle/Inventory/Mchenry.xlsx'
        super().__init__(mfr)

    def parse_file_to_dictionary(self):
        products = {}
        workbook = xlrd.open_workbook(self.distributor_inventory_filepath)
        workbook = xlrd.open_workbook(self.distributor_inventory_filepath, on_demand=True)
        worksheet = workbook.sheet_by_index(0)
        first_row = []  # The row where we stock the name of the column
        for col in range(worksheet.ncols):
            first_row.append(worksheet.cell_value(0, col))
        # transform the workbook to a list of dictionaries
        data = []
        for row in range(1, worksheet.nrows):
            elm = {}
            for col in range(worksheet.ncols):
                elm[first_row[col]] = worksheet.cell_value(row, col)
            data.append(elm)
        try:
            for row in data:
                len_pid = len(row['Item Code'])
                item_code = row['Item Code']
                product_id = item_code[5:len_pid]
                row['Product ID'] = product_id
                row['Fulfillment Source'] = 'Drop Shipper'
                row['Action'] = 'Reconcileto'
                row['Error'] = ''
                products[row['Product ID']] = dict(row)
        except:
            pass
        return products
