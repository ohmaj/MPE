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
import threading

class RunAll:
    results_filepath = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + 'web.csv'

    def run(self):
        self.cls()
        kaw = Distributor_Kawasaki.Kawasaki('KAW')
        kaw.save_to_filepath = self.results_filepath
        arn = Distributor_Ariens.Ariens('ARN')
        arn.save_to_filepath = self.results_filepath
        aip = Distributor_AIP.AIP('AIP')
        aip.save_to_filepath = self.results_filepath
        # th1 = threading.Thread(target=self.golden_eagle)
        th2 = threading.Thread(target=kaw.write_inventory)
        th3 = threading.Thread(target=aip.write_inventory)
        th4 = threading.Thread(target=arn.write_inventory)
        # th1.start()
        th2.start()
        th3.start()
        th4.start()
        input('Press Enter To Finish')
    #
    # def golden_eagle(self):
    #     bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
    #     bil.save_to_filepath = self.results_filepath
    #     bil.write_inventory()
    #     ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
    #     ech.save_to_filepath = self.results_filepath
    #     ech.write_inventory()

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
