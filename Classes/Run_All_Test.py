from Classes import Distributor_Kawasaki
from Classes import Distributor_Golden_Eagle
from Classes import Distributor_Ariens
from Classes import Distributor_AIP
from Classes import From_File_OscarWilson
from Classes import From_File_Stens
from Classes import XML_CPD
from Classes import Ideal_Scrape
import time
import os
import csv


class RunAll:
    save_to_filepath = r'T:/ebay/All/inventory/All_test_' + time.strftime('%m%d%Y' + '_' + '%I%M') + '.csv'
    header = False

    def run(self):
        self.cls()
        kaw = Distributor_Kawasaki.Kawasaki('KAW')
        ic = XML_CPD.CPD('IC')
        hyd = XML_CPD.CPD('HYD')
        tec = XML_CPD.CPD('TEC')
        koh = XML_CPD.CPD('KOH')
        ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
        bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
        arn = Distributor_Ariens.Ariens('ARN')
        aip = Distributor_AIP.AIP('AIP')
        mtd = From_File_OscarWilson.UpdateInventory('MTD')
        mar = From_File_OscarWilson.UpdateInventory('MAR')
        ste = From_File_Stens.Update_Inventory()
        ideal = Ideal_Scrape.DatabaseConnection()
        try:
            ech_inventory = ech.get_inventory()
            ech_success = 'Echo Update Successful'
            self.write_dict_to_csv(ech_inventory)
        except:
            ech_success = 'Error Updating Echo'
        try:
            bil_inventory = bil.get_inventory()
            bil_success = 'Billy Goat Update Successful'
            self.write_dict_to_csv(bil_inventory)
        except:
            bil_success = 'Error Updating BillyGoat'
        try:
            aip_inventory = aip.get_inventory()
            aip_success = 'A&I Update Successful'
            self.write_dict_to_csv(aip_inventory)
        except:
            aip_success = 'Error Updating A&I'
        try:
            mtd_inventory = mtd.get_inventory()
            mtd_success = 'MTD Update Successful'
            self.write_dict_to_csv(mtd_inventory)
        except:
            mtd_success = 'Error Updating MTD'
        try:
            mar_inventory = mar.get_inventory()
            mar_success = 'MAR Update Successful'
            self.write_dict_to_csv(mar_inventory)
        except:
            mar_success = 'Error Updating MAR'
        try:
            ste_inventory = ste.get_inventory()
            ste_success = 'Stens Update Successful'
            self.write_dict_to_csv(ste_inventory)
        except:
            ste_success = 'Error Updating Stens'
        try:
            ic_inventory = ic.get_inventory()
            ic_success = 'Case Update Successful'
            self.write_dict_to_csv(ic_inventory)
        except:
            ic_success = 'Error Updating Case'
        try:
            hyd_inventory = hyd.get_inventory()
            hyd_success = 'Hydro Gear Update Successful'
            self.write_dict_to_csv(hyd_inventory)
        except:
            hyd_success = 'Error Updating Hydro Gear'
        try:
            tec_inventory = tec.get_inventory()
            tec_success = 'Tecumseh Update Successful'
            self.write_dict_to_csv(tec_inventory)
        except:
            tec_success ='Error Updating Tecumseh'
        try:
            koh_inventory = koh.get_inventory()
            koh_success = 'Kohler Update Successful'
            self.write_dict_to_csv(koh_inventory)
        except:
            koh_success = 'Error Updating Kohler'
        try:
            arn_inventory = arn.get_inventory()
            arn_success = 'Ariens Update Successful'
            self.write_dict_to_csv(arn_inventory)
        except:
            arn_success = 'Error Updating Ariens'
        try:
            kaw_inventory = kaw.get_inventory()
            kaw_success = 'Kawasaki Update Successful'
            self.write_dict_to_csv(kaw_inventory)
        except:
            kaw_success = 'Error Updating Kawasaki'
        try:
            ideal_inventory = ideal.get_inventory()
            ideal_success = 'Self Update Successful'
            self.write_dict_to_csv(ideal_inventory)
        except:
            ideal_success = 'Error Updating Self'
        print_list = [mtd_success, mar_success,ste_success, ic_success, hyd_success, tec_success, koh_success,
                      ech_success, bil_success, arn_success, aip_success, kaw_success, ideal_success]
        for item in print_list:
            print(item)
        input('Press Enter To Finish')

    def write_dict_to_csv(self, updated_products):
        ordered_dicts = [{'Item ID' : product['Item ID'],
                          'External Item ID':product['External Item ID'],
                          'SKU' : product['SKU'],
                          'Product ID' : product['Product ID'],
                          'Storage Location' : product['Storage Location'],
                          'Quantity' : product['Quantity'],
                          'Cost' : product['Cost'],
                          'Supplier ID' : product['Supplier ID'],
                          'Supplier Account Num' : product['Supplier Account Num'],
                          'Supplier Name' : product['Supplier Name'],
                          'Date Purchased' : product['Date Purchased'],
                          'Fulfillment Source': 'Drop Shipper',
                          'PO Number' : product['PO Number'],
                          'Invoice Number' : product['Invoice Number'],
                          'Action': 'Reconcileto'
                          } for product in updated_products]
        print('Writing File....')
        keys = ordered_dicts[0].keys()
        with open(self.save_to_filepath, 'a', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            if not self.header:
                dict_writer.writeheader()
                self.header = True
            dict_writer.writerows(ordered_dicts)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')


run_all = RunAll()
run_all.run()
