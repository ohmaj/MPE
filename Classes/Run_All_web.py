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
        results_filepath = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + 'web.csv'

        try:
            aip = Distributor_AIP.AIP('AIP')
            aip.save_to_filepath = results_filepath
            aip.write_inventory()
            aip_success = 'A&I Update Successful'
        except:
            aip_success = 'Error Updating A&I'
        try:
            arn = Distributor_Ariens.Ariens('ARN')
            arn.save_to_filepath = results_filepath
            arn.write_inventory()
            arn_success = 'Ariens Update Successful'
        except:
            arn_success = 'Error Updating Ariens'
        try:
            ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
            ech.save_to_filepath = results_filepath
            ech.write_inventory()
            ech_success = 'Echo Update Successful'
        except:
            ech_success = 'Error Updating Echo'
        try:
            bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
            bil.save_to_filepath = results_filepath
            bil.write_inventory()
            bil_success = 'Billy Goat Update Successful'
        except:
            bil_success = 'Error Updating BillyGoat'
        try:
            kaw = Distributor_Kawasaki.Kawasaki('KAW')
            kaw.save_to_filepath = results_filepath
            kaw.write_inventory()
            kaw_success = 'Kawasaki Update Successful'
        except:
            kaw_success = 'Error Updating Kawasaki'
        print_list = [ech_success, bil_success, arn_success, aip_success, kaw_success]
        for item in print_list:
            print(item)
        input('Press Enter To Finish')

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
