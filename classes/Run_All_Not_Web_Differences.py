from classes import From_File_OscarWilson
from classes import From_File_Stens
from classes import XML_CPD
from classes import Ideal_Scrape
from classes import From_File_Golden_Eagle
import time
import os


class RunAll:

    def run(self):
        self.cls()
        results_filepath = r'T:/ebay/All/inventory/All_new_' + time.strftime('%m%d%Y' + '_' + '%I%M') + 'self.csv'
        try:
            print('starting1')
            bil = From_File_Golden_Eagle.GoldenEagleFromFile("BIL")
            bil.write_to_filepath = results_filepath
            bil.write_inventory_changes()
            print('BIL Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting2')
            ech = From_File_Golden_Eagle.GoldenEagleFromFile("ECH")
            ech.write_to_filepath = results_filepath
            ech.write_inventory_changes()
            print('ECH Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting3')
            mtd = From_File_OscarWilson.UpdateInventory('MTD')
            mtd.save_to_filepath = results_filepath
            mtd.write_inventory_changes()
            print('MTD Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting4')
            mar = From_File_OscarWilson.UpdateInventory('MAR')
            mar.save_to_filepath = results_filepath
            mar.write_inventory_changes()
            print('MAR Update Successful')
        except Exception as inst:
            print(nst.__str__())
        try:
            print('starting5')
            ste = From_File_Stens.Update_Inventory()
            ste.save_to_filepath = results_filepath
            ste.write_inventory_changes()
            print('Stens Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting6')
            ic = XML_CPD.CPD('IC')
            ic.save_to_filepath = results_filepath
            ic.write_inventory_changes()
            print('Case Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting7')
            hyd = XML_CPD.CPD('HYD')
            hyd.save_to_filepath = results_filepath
            hyd.write_inventory_changes()
            print('Hydro Gear Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting8')
            tec = XML_CPD.CPD('TEC')
            tec.save_to_filepath = results_filepath
            tec.write_inventory_changes()
            print('Tecumseh Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting9')
            koh = XML_CPD.CPD('KOH')
            koh.save_to_filepath = results_filepath
            koh.write_inventory_changes()
            print('Kohler Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting10')
            ayp = XML_CPD.CPD('AYP')
            ayp.save_to_filepath = results_filepath
            ayp.write_inventory_changes()
            print('AYP Update Successful')
        except Exception as inst:
            print(inst.__str__())
        try:
            print('starting11')
            ideal = Ideal_Scrape.Database()
            ideal.save_to_filepath = results_filepath
            ideal.write_inventory_changes()
            print('Self Update Successful')
        except Exception as inst:
            print(inst.__str__())
    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')


runall = RunAll()
runall.run()
