from classes import Scrape_Kawasaki
from classes import Scrape_Golden_Eagle
from classes import Scrape_Ariens
from classes import Scrape_AIP
from classes import From_File_OscarWilson
from classes import From_File_Stens
from classes import XML_CPD
from classes import Ideal_Scrape
import time
import os
import threading

class RunAll:
    results_filepath = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + 'web.csv'

    def run(self):
        self.cls()
        kaw = Scrape_Kawasaki.Kawasaki('KAW')
        kaw.save_to_filepath = self.results_filepath
        arn = Scrape_Ariens.Ariens('ARN')
        arn.save_to_filepath = self.results_filepath
        aip = Scrape_AIP.AIP('AIP')
        aip.save_to_filepath = self.results_filepath
        # th1 = threading.Thread(target=self.golden_eagle)
        th2 = threading.Thread(target=kaw.write_inventory_changes)
        th3 = threading.Thread(target=aip.write_inventory_changes)
        th4 = threading.Thread(target=arn.write_inventory_changes)
        # th1.start()
        th2.start()
        th3.start()
        th4.start()
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


runall = RunAll()
runall.run()
