from Classes import goldenEagleDealer
from Classes import kawasakiDealer
from Classes import ariensDealer
from Classes import aipDealer
from Classes import From_File_OscarWilson
from Classes import XML_CPD
import time
import os

class Run_All:

    def run(self):
        self.cls()
        resultsFilePath = r'T:/ebay/All/inventory/All_Results_' + time.strftime('%m%d%Y' + '_' + '%I%M') + '.csv'
        ic = XML_CPD.CPD('IC')
        ic.save_to_filepath = resultsFilePath
        hyd = XML_CPD.CPD('HYD')
        hyd.save_to_filepath = resultsFilePath
        tec = XML_CPD.CPD('TEC')
        tec.save_to_filepath = resultsFilePath
        koh = XML_CPD.CPD('KOH')
        koh.save_to_filepath = resultsFilePath
        ech = goldenEagleDealer.GoldenEagle('ECH')
        ech.resultsFilePath = resultsFilePath
        bil = goldenEagleDealer.GoldenEagle('BIL')
        bil.resultsFilePath = resultsFilePath
        arn = ariensDealer.Ariens()
        arn.resultsFilePath = resultsFilePath
        kaw = kawasakiDealer.Kawasaki()
        kaw.resultsFilePath = resultsFilePath
        aip = aipDealer.AIP()
        aip.resultsFilePath = resultsFilePath
        mtd = From_File_OscarWilson.Update_Inventory('MTD')
        mtd.save_to_filepath = resultsFilePath
        mar = From_File_OscarWilson.Update_Inventory('MAR')
        mar.save_to_filepath = resultsFilePath
        try:
            arn.get_update()
            arn_success ='Ariens Update Successful'
        except:
            arn_success ='Error Updating Ariens'
        try:
            ech.get_update()
            ech_success ='Echo Update Successful'
        except:
            ech_success ='Error Updating Echo'
        try:
            bil.get_update()
            bil_success ='Billy Goat Update Successful'
        except:
            bil_success ='Error Updating BillyGoat'
        try:
            kaw.get_update()
            kaw_success ='Kawasaki Update Successful'
        except:
            kaw_success ='Error Updating Kawasaki'
        try:
            aip.get_update()
            aip_success ='A&I Update Successful'
        except:
            aip_success ='Error Updating A&I'
        try:
            mtd.get_update()
            mtd_success = 'Case Update Successful'
        except:
            mtd_success = 'Error Updating Case'
        try:
            mar.get_update()
            mar_success = 'Case Update Successful'
        except:
            mar_success = 'Error Updating Case'
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
        print_list = [mtd_success, mar_success, ic_success, hyd_success, tec_success, koh_success, ech_success, bil_success, arn_success, aip_success, kaw_success]
        for item in print_list:
            print(item)
        input('Press Enter To Finsih')

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')