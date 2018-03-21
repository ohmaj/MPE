from Classes import Distributor_Kawasaki
from Classes import Distributor_Ariens
from Classes import Distributor_AIP
import time
import os
import threading


class RunAll:
    results_filepath = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + 'web.csv'

    def run(self):
        self.cls()
        kaw = Distributor_Kawasaki.Kawasaki('KAW')
        kaw.save_to_filepath = self.results_filepath
        arn1 = Distributor_Ariens.Ariens('ARN')
        arn1.save_to_filepath = self.results_filepath
        arn2 = Distributor_Ariens.Ariens('ARN')
        arn2.save_to_filepath = self.results_filepath
        aip = Distributor_AIP.AIP('AIP')
        aip.save_to_filepath = self.results_filepath
        th2 = threading.Thread(target=kaw.write_inventory)
        th3 = threading.Thread(target=aip.write_inventory)
        th4 = threading.Thread(target=arn1.write_inventory_threaded, kwargs=dict(number_batches=2, number_batch=0))
        th5 = threading.Thread(target=arn2.write_inventory_threaded, kwargs=dict(number_batches=2, number_batch=1))
        th2.start()
        th3.start()
        th4.start()
        th5.start()

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')
