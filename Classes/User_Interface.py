from Classes import Distributor_Golden_Eagle
from Classes import Distributor_Kawasaki
from Classes import Distributor_Ariens
from Classes import Distributor_AIP
from Classes import XML_CPD
from Classes import From_File_OscarWilson
from Classes import Run_All
from Classes import Ideal_Scrape
import sys
import os

class User_Interface:

    def main_menu(self):
        self.cls()
        print('Main Menu \n ------------ \n [1]Golden Eagle [2] Ariens [3] Kawasaki [4] AIP [5] CPD [6] Oscar Wilson [7] Ideal [8] Run All [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            self.golden_eagle_menu()
        elif userSelection == '2':
            self.ariens_menu()
        elif userSelection == '3':
            self.kawasaki_menu()
        elif userSelection == '4':
            self.aip_menu()
        elif userSelection == '5':
            self.cpd_menu()
        elif userSelection == '6':
            self.ow_menu()
        elif userSelection == '7':
            ideal = Ideal_Scrape.database_connection()
            ideal.main()
        elif userSelection == '8':
            all = Run_All.Run_All()
            all.run()
        elif userSelection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.main_menu()
        self.main_menu()

    def run_all(self):
        all = Run_All.Run_All()
        all.run()
        self.main_menu()

    def aip_menu(self):
        self.cls()
        print('Main Menu \n ------------ \n [1] Quantity Scrape [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            aip = Distributor_AIP.AIP('AIP')
            aip.scrape_inventory()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def cpd_menu(self):
        self.cls()
        print('Main Menu \n ------------ \n [1]XML Inquiry Quantity [2] Get XML Response Only [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            self.cpd_xml_menu()
        elif userSelection == '2':
            self.cpd_xml_response()
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

    def kawasaki_menu(self):
        self.cls()
        print('CPD Scrape Menu \n ------------ \n [1] Scrape Kawasaki [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            kaw = Distributor_Kawasaki.Kawasaki('KAW')
            kaw.scrape_inventory()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def ariens_menu(self):
        self.cls()
        print('CPD Scrape Menu \n ------------ \n [1] Scrape Ariens [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            ariens = Distributor_Ariens.Ariens('ARN')
            ariens.scrape_inventory()
        elif userSelection == 'back':
            self.main_menu()
        elif userSelection == 'exit':
            sys.exit()

    def golden_eagle_menu(self):
        self.cls()
        print('CPD Scrape Menu \n ------------ \n [1] Scrape Echo [2] Scrape Billygoat [3] Scrape Both [back] Back to Main Menu [exit] Exit Program')
        userSelection = input('What would you like to do?: ')
        if userSelection == '1':
            ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
            ech.scrape_inventory()
        elif userSelection == '2':
            bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
            bil.scrape_inventory()
        elif userSelection == '3':
            ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
            bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
            ech.scrape_inventory()
            bil.scrape_inventory()
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
            koh.get_xml_response()
        elif userSelection == '2':
            tec = XML_CPD.CPD('TEC')
            tec.get_xml_response()
        elif userSelection == '3':
            hyg = XML_CPD.CPD('HYD')
            hyg.get_xml_response()
        elif userSelection == '4':
            ic = XML_CPD.CPD('IC')
            ic.get_xml_response()
        elif userSelection == '5':
            try:
                koh = XML_CPD.CPD('KOH')
                koh.get_xml_response()
            except:
                pass
            try:
                tec = XML_CPD.CPD('TEC')
                tec.get_xml_response()
            except:
                pass
            try:
                hyg = XML_CPD.CPD('HYD')
                hyg.get_xml_response()
            except:
                pass
            try:
                case = XML_CPD.CPD('IC')
                case.get_xml_response()
            except:
                pass
        elif userSelection == 'back':
            self.cpd_menu()
        elif userSelection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.cpd_xml_response()
        self.cpd_xml_response()

    def cpd_xml_response(self):
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

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

program = User_Interface()
program.main_menu()