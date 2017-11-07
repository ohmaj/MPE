from Classes import Distributor_Kawasaki
from Classes import Distributor_Golden_Eagle
from Classes import Distributor_Ariens
from Classes import Distributor_AIP
from Classes import From_File_OscarWilson
from Classes import XML_CPD
from Classes import Ideal_Scrape
import time
import os

class Run_All:

    def run(self):
        self.cls()
        results_filepath = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + '.csv'
        kaw = Distributor_Kawasaki.Kawasaki('KAW')
        kaw.save_to_filepath = results_filepath
        ic = XML_CPD.CPD('IC')
        ic.save_to_filepath = results_filepath
        hyd = XML_CPD.CPD('HYD')
        hyd.save_to_filepath = results_filepath
        tec = XML_CPD.CPD('TEC')
        tec.save_to_filepath = results_filepath
        koh = XML_CPD.CPD('KOH')
        koh.save_to_filepath = results_filepath
        ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
        ech.save_to_filepath = results_filepath
        bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
        bil.save_to_filepath = results_filepath
        arn = Distributor_Ariens.Ariens('ARN')
        arn.save_to_filepath = results_filepath
        aip = Distributor_AIP.AIP('AIP')
        aip.save_to_filepath = results_filepath
        mtd = From_File_OscarWilson.Update_Inventory('MTD')
        mtd.save_to_filepath = results_filepath
        mar = From_File_OscarWilson.Update_Inventory('MAR')
        mar.save_to_filepath = results_filepath
        ideal = Ideal_Scrape.database_connection()
        ideal.save_to_filepath = results_filepath
        try:
            ech.scrape_inventory()
            ech_success ='Echo Update Successful'
        except:
            ech_success ='Error Updating Echo'
        try:
            bil.scrape_inventory()
            bil_success ='Billy Goat Update Successful'
        except:
            bil_success ='Error Updating BillyGoat'
        try:
            aip.scrape_inventory()
            aip_success ='A&I Update Successful'
        except:
            aip_success ='Error Updating A&I'
        try:
            mtd.get_update()
            mtd_success = 'MTD Update Successful'
        except:
            mtd_success = 'Error Updating MTD'
        try:
            mar.get_update()
            mar_success = 'MAR Update Successful'
        except:
            mar_success = 'Error Updating MAR'
        try:
            ic.get_update()
            ic_success = 'Case Update Successful'
        except:
            ic_success = 'Error Updating Case'
        try:
            hyd.get_update()
            hyd_success ='Hydro Gear Update Successful'
        except:
            hyd_success ='Error Updating Hydro Gear'
        try:
            tec.get_update()
            tec_success ='Tecumseh Update Successful'
        except:
            tec_success ='Error Updating Tecumseh'
        try:
            koh.get_update()
            koh_success ='Kohler Update Successful'
        except:
            koh_success ='Error Updating Kohler'
        try:
            arn.scrape_inventory()
            arn_success ='Ariens Update Successful'
        except:
            arn_success ='Error Updating Ariens'
        try:
            kaw.scrape_inventory()
            kaw_success = 'Kawasaki Update Successful'
        except:
            kaw_success = 'Error Updating Kawasaki'
        try:
            ideal.main()
            ideal_success ='Self Update Successful'
        except:
            ideal_success ='Error Updating Self'
        print_list = [mtd_success, mar_success, ic_success, hyd_success, tec_success, koh_success, ech_success, bil_success, arn_success, aip_success, kaw_success, ideal_success]
        for item in print_list:
            print(item)
        input('Press Enter To Finish')

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')