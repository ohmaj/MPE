from Classes import Distributor_AIP
import time
import os
import threading


class ThreadingAIP:
    results_filepath = r'T:/ebay/AIP/DATA/2018/best sellers/Full_inventory' + time.strftime('%I%M') + '.csv'

    def run(self):
        self.cls()
        aip0 = Distributor_AIP.AIP('AIP')
        aip0.save_to_filepath = self.results_filepath
        aip1 = Distributor_AIP.AIP('AIP')
        aip1.save_to_filepath = self.results_filepath
        aip2 = Distributor_AIP.AIP('AIP')
        aip2.save_to_filepath = self.results_filepath
        aip3 = Distributor_AIP.AIP('AIP')
        aip3.save_to_filepath = self.results_filepath
        aip4 = Distributor_AIP.AIP('AIP')
        aip4.save_to_filepath = self.results_filepath
        aip5 = Distributor_AIP.AIP('AIP')
        aip5.save_to_filepath = self.results_filepath
        aip6 = Distributor_AIP.AIP('AIP')
        aip6.save_to_filepath = self.results_filepath
        aip7 = Distributor_AIP.AIP('AIP')
        aip7.save_to_filepath = self.results_filepath
        aip8 = Distributor_AIP.AIP('AIP')
        aip8.save_to_filepath = self.results_filepath
        aip9 = Distributor_AIP.AIP('AIP')
        aip9.save_to_filepath = self.results_filepath
        th0 = threading.Thread(target=aip0.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=0))
        th1 = threading.Thread(target=aip1.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=1))
        th2 = threading.Thread(target=aip2.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=2))
        th3 = threading.Thread(target=aip3.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=3))
        th4 = threading.Thread(target=aip4.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=4))
        th5 = threading.Thread(target=aip5.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=5))
        th6 = threading.Thread(target=aip6.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=6))
        th7 = threading.Thread(target=aip7.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=7))
        th8 = threading.Thread(target=aip8.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=8))
        th9 = threading.Thread(target=aip9.write_inventory_threaded, kwargs=dict(number_batches=10, number_batch=9))
        th0.start()
        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th5.start()
        th6.start()
        th7.start()
        th8.start()
        th9.start()

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')


threading_aip = ThreadingAIP()
threading_aip.run()
