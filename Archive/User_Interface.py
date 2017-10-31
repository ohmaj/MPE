from Classes import goldenEagleDealer
from Classes import kawasakiDealer
from Classes import ariensDealer
from Classes import aipDealer
from Classes import aipProductInfo
from Classes import cpdDealer
from Classes import XML_CPD
from Classes import From_File_OscarWilson
from Classes import Run_All
import sys
import os

class User_Interface:

    def main_menu(self):
        self.cls()
        print('Main Menu \n ------------ \n [1]Golden Eagle [2] Ariens [3] Kawasaki [4] AIP [5] CPD [6] Oscar Wilson [7] Run All [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            self.golden_eagle()
        elif userSelection == '2':
            self.ariens()
        elif userSelection == '3':
            self.kawasaki()
        elif userSelection == '4':
            self.aip()
        elif userSelection == '5':
            self.cpd_menu()
        elif userSelection == '6':
            self.ow_menu()
        elif userSelection == '7':
            all = Run_All.Run_All()
            all.run()
        elif userSelection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.main_menu()
        self.main_menu()

    def aip(self):
        self.cls()
        print('Main Menu \n ------------ \n [1] Quantity Scrape [2] Product Info Scrape [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            aip = aipDealer.AIP()
            aip.get_update()
        elif userSelection == '2':
            aipInfo = aipProductInfo.AIP()
            aipInfo.get_update()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def cpd_menu(self):
        self.cls()
        print('Main Menu \n ------------ \n [1]XML Inquiry[back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            self.cpd_xml_menu()
        # elif userSelection == '2':
        #     self.cpd_scrape_menu()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def ow_menu(self):
        self.cls()
        print('Oscar Wilson Menu \n ------------ \n [1] Update MTD [2] Update Maruyama [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            mtd_update = From_File_OscarWilson.Update_Inventory('MTD')
            mtd_update.get_update()
        if userSelection == '2':
            mar_update = From_File_OscarWilson.Update_Inventory('MAR')
            mar_update.get_update()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def kawasaki(self):
        self.cls()
        print('CPD Scrape Menu \n ------------ \n [1] Scrape Kawasaki [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            manufacturer = kawasakiDealer.Kawasaki()
            manufacturer.get_update()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def ariens(self):
        self.cls()
        print('CPD Scrape Menu \n ------------ \n [1] Scrape Ariens [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            ariens = ariensDealer.Ariens()
            ariens.get_update()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def golden_eagle(self):
        self.cls()
        print('CPD Scrape Menu \n ------------ \n [1] Scrape Echo [2] Scrape Billygoat [3] Scrape Both [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            ech = goldenEagleDealer.GoldenEagle('ECH')
            ech.get_update()
        elif userSelection == '2':
            bil = goldenEagleDealer.GoldenEagle('BIL')
            bil.get_update()
        elif userSelection == '3':
            ech = goldenEagleDealer.GoldenEagle('ECH')
            bil = goldenEagleDealer.GoldenEagle('BIL')
            ech.get_update()
            bil.get_update()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def cpd_xml_menu(self):
        self.cls()
        print('CPD Scrape Menu \n ------------ \n [1] Kohler [2] Tecumseh [3] Hydro Gear [4] Case [5] All [back] Back to CPD Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            koh = XML_CPD.CPD('KOH')
            koh.get_update()
        elif userSelection == '2':
            tec = XML_CPD.CPD('TEC')
            tec.get_update()
        elif userSelection == '3':
            hyg = XML_CPD.CPD('HYD')
            hyg.get_update()
        elif userSelection == '4':
            ic = XML_CPD.CPD('IC')
            ic.get_update()
        elif userSelection == '5':
            try:
                koh = XML_CPD.CPD('KOH')
                koh.get_update()
            except:
                pass
            try:
                tec = XML_CPD.CPD('TEC')
                tec.get_update()
            except:
                pass
            try:
                hyg = XML_CPD.CPD('HYD')
                hyg.get_update()
            except:
                pass
            try:
                case = XML_CPD.CPD('IC')
                case.get_update()
            except:
                pass
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.cpd_xml_menu()
        self.cpd_xml_menu()

    # def cpd_scrape_menu(self):
    #     self.cls()
    #     print('CPD Scrape Menu \n ------------ \n [1] Scrape Kohler [2] Scrape Tecumseh [3] Scrape Hydro Gear [4] Scrape Case [5] Scrape All [back] Back to CPD [exit] Exit Program')
    #     userSelection = input('What would you like to do?: ')
    #     if userSelection == '1':
    #         koh = cpdDealer.CPD('KOHLER')
    #         koh.get_update()
    #     elif userSelection == '2':
    #         tec = cpdDealer.CPD('TEC')
    #         tec.get_update()
    #     elif userSelection == '3':
    #         hyg = cpdDealer.CPD('HYD')
    #         hyg.get_update()
    #     elif userSelection == '4':
    #         case = cpdDealer.CPD('CASE')
    #         case.get_update()
    #     elif userSelection == '5':
    #         try:
    #             koh = cpdDealer.CPD('KOHLER')
    #             koh.get_update()
    #         except:
    #             pass
    #         try:
    #             tec = cpdDealer.CPD('TEC')
    #             tec.get_update()
    #         except:
    #             pass
    #         try:
    #             hyg = cpdDealer.CPD('HYD')
    #             hyg.get_update()
    #         except:
    #             pass
    #         try:
    #             case = cpdDealer.CPD('CASE')
    #             case.get_update()
    #         except:
    #             pass
    #     elif userSelection == 'exit':
    #         sys.exit()
    #     elif userSelection == 'back':
    #         self.cpd_menu()
    #     else:
    #         print('That is not a valid selection please choose from the available options')
    #         self.cpd_scrape_menu()
    #     self.cpd_scrape_menu()

    # def scrape_aip_product_info(self):
    #     self.cls()
    #     print('Product Info Menu \n ------------ \n [1] Scrape AIP Qty [back] AIP Menu [exit] Exit Program')
    #     userSelection = input('What would you like to do?: ')
    #     if userSelection == '1':
    #         aipInfo = aipProductInfo.AIP()
    #         aipInfo.get_update()
    #     elif userSelection == 'back':
    #         self.aip()
    #     elif userSelection == 'exit':
    #         sys.exit()
    #     else:
    #         print('That is not a valid selection please choose from the available options')
    #         self.scrape_aip_product_info()
    #     self.scrape_aip_product_info()

    # def scrape_aip_qty(self):
    #     self.cls()
    #     print('Product Info Menu \n ------------ \n [1] Scrape AIP Product Info [back] AIP Menu [exit] Exit Program')
    #     userSelection = input('What would you like to do?: ')
    #     if userSelection == '1':
    #         aip = aipDealer.AIP()
    #         aip.get_update()
    #     elif userSelection == 'back':
    #         self.aip()
    #     elif userSelection == 'exit':
    #         sys.exit()
    #     else:
    #         print('That is not a valid selection please choose from the available options')
    #         self.scrape_aip_qty()
    #     self.scrape_aip_qty()
    #
    # def cls(self):
    #     os.system('cls' if os.name == 'nt' else 'clear')

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')