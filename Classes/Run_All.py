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


class RunAll:

    def run(self):
        self.cls()
        results_filepath = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + 'self.csv'
        results_filepath_web = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + 'web.csv'
        try:
            mtd = From_File_OscarWilson.UpdateInventory('MTD')
            mtd.save_to_filepath = results_filepath
            mtd.write_inventory()
            mtd_success = 'MTD Update Successful'
        except:
            mtd_success = 'Error Updating MTD'
        try:
            mar = From_File_OscarWilson.UpdateInventory('MAR')
            mar.save_to_filepath = results_filepath
            mar.write_inventory()
            mar_success = 'MAR Update Successful'
        except:
            mar_success = 'Error Updating MAR'
        try:
            ste = From_File_Stens.Update_Inventory()
            ste.save_to_filepath = results_filepath
            ste.write_inventory()
            ste_success = 'Stens Update Successful'
        except:
            ste_success = 'Error Updating Stens'
        try:
            ic = XML_CPD.CPD('IC')
            ic.save_to_filepath = results_filepath
            ic.write_inventory()
            ic_success = 'Case Update Successful'
        except:
            ic_success = 'Error Updating Case'
        try:
            hyd = XML_CPD.CPD('HYD')
            hyd.save_to_filepath = results_filepath
            hyd.write_inventory()
            hyd_success = 'Hydro Gear Update Successful'
        except:
            hyd_success = 'Error Updating Hydro Gear'
        try:
            tec = XML_CPD.CPD('TEC')
            tec.save_to_filepath = results_filepath
            tec.write_inventory()
            tec_success = 'Tecumseh Update Successful'
        except:
            tec_success = 'Error Updating Tecumseh'
        try:
            koh = XML_CPD.CPD('KOH')
            koh.save_to_filepath = results_filepath
            koh.write_inventory()
            koh_success = 'Kohler Update Successful'
        except:
            koh_success = 'Error Updating Kohler'
        try:
            ideal = Ideal_Scrape.DatabaseConnection()
            ideal.save_to_filepath = results_filepath
            ideal.write_inventory()
            ideal_success = 'Self Update Successful'
        except:
            ideal_success = 'Error Updating Self'
        print(ideal_success)
        try:
            aip = Distributor_AIP.AIP('AIP')
            aip.save_to_filepath = results_filepath_web
            aip.write_inventory()
            aip_success = 'A&I Update Successful'
        except:
            aip_success = 'Error Updating A&I'
        try:
            arn = Distributor_Ariens.Ariens('ARN')
            arn.save_to_filepath = results_filepath_web
            arn.write_inventory()
            arn_success = 'Ariens Update Successful'
        except:
            arn_success = 'Error Updating Ariens'
        try:
            ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
            ech.save_to_filepath = results_filepath_web
            ech.write_inventory()
            ech_success = 'Echo Update Successful'
        except:
            ech_success = 'Error Updating Echo'
        try:
            bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
            bil.save_to_filepath = results_filepath_web
            bil.write_inventory()
            bil_success = 'Billy Goat Update Successful'
        except:
            bil_success = 'Error Updating BillyGoat'
        try:
            kaw = Distributor_Kawasaki.Kawasaki('KAW')
            kaw.save_to_filepath = results_filepath_web
            kaw.write_inventory()
            kaw_success = 'Kawasaki Update Successful'
        except:
            kaw_success = 'Error Updating Kawasaki'
        print_list = [mtd_success, mar_success,ste_success, ic_success, hyd_success, tec_success, koh_success, ech_success, bil_success, arn_success, aip_success, kaw_success, ideal_success]
        for item in print_list:
            print(item)
        input('Press Enter To Finish')

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
