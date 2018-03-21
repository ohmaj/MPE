from Classes import Distributor_Golden_Eagle
from Classes import Distributor_Kawasaki
from Classes import Distributor_Ariens
from Classes import Distributor_AIP
from Classes import XML_CPD
from Classes import From_File_OscarWilson
from Classes import Run_All_web
from Classes import Run_All_Not_Web
from Classes import Ideal_Scrape
from Classes import From_File_Golden_Eagle
import sys
import os
import time


class UserInterface:

    def main_menu(self):
        self.cls()
        print('Main Menu \n ------------ \n[1] Golden Eagle \n[2] Ariens \n[3] Kawasaki \n[4] AIP \n[5] CPD \n'
              '[6] Oscar Wilson \n[7] Ideal \n[8] Run All \n[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            self.golden_eagle_menu()
        elif user_selection == '2':
            self.ariens_menu()
        elif user_selection == '3':
            self.kawasaki_menu()
        elif user_selection == '4':
            self.aip_menu()
        elif user_selection == '5':
            self.cpd_menu()
        elif user_selection == '6':
            self.ow_menu()
        elif user_selection == '7':
            ideal = Ideal_Scrape.DatabaseConnection()
            ideal.write_inventory()
        elif user_selection == '8':
            self.run_all()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.main_menu()
        self.main_menu()

    def run_all(self):
        print('Run All Menu \n ------------ \n[1] All Web Scrapes \n[2] All Other \n[3] All The All'
              '\n[back] Back to Main Menu \n[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            run_all = Run_All_web.RunAll()
            run_all.run()
        elif user_selection == '2':
            run_all = Run_All_Not_Web.RunAll()
            run_all.run()
        elif user_selection == '3':
            run_all = Run_All_Not_Web.RunAll()
            run_all.run()
            run_all_scrapes = Run_All_web.RunAll()
            run_all_scrapes.run()
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.run_all()
        self.run_all()

    def aip_menu(self):
        self.cls()
        print('A&I Products Menu \n ------------ \n[1] Quantity Scrape '
              '\n[back] Back to Main Menu \n[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            aip = Distributor_AIP.AIP('AIP')
            aip.write_inventory()
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.aip_menu()

        self.aip_menu()

    def cpd_menu(self):
        self.cls()
        print('CPD Menu \n ------------ \n[1] XML Inquiry Quantity \n[2] Get XML Response Only '
              '\n[back] Back to Main Menu \n[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            self.cpd_xml_menu()
        elif user_selection == '2':
            self.cpd_xml_response()
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.cpd_menu()

        self.cpd_menu()

    def ow_menu(self):
        self.cls()
        print('Oscar Wilson Menu \n ------------ \n[1] MTD \n[2] Maruyama \n[3] AYP \n[back] Back to Main Menu '
              '\n[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            mtd = From_File_OscarWilson.UpdateInventory('MTD')
            mtd.write_inventory()
        elif user_selection == '2':
            mar = From_File_OscarWilson.UpdateInventory('MAR')
            mar.write_inventory()
        elif user_selection == '3':
            ayp = From_File_OscarWilson.UpdateInventory('AYP')
            ayp.write_inventory()
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.ow_menu()

        self.ow_menu()

    def kawasaki_menu(self):
        self.cls()
        print('Kawasaki Menu \n ------------ \n[1] Scrape Kawasaki \n[back] Back to Main Menu \n'
              '[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            kaw = Distributor_Kawasaki.Kawasaki('KAW')
            kaw.write_inventory()
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.kawasaki_menu()

        self.kawasaki_menu()

    def ariens_menu(self):
        self.cls()
        print('Ariens Menu \n ------------ \n[1] Scrape Ariens \n[back] Back to Main Menu \n[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            ariens = Distributor_Ariens.Ariens('ARN')
            ariens.write_inventory()
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.ariens_menu()

        self.ariens_menu()

    def golden_eagle_menu(self):
        self.cls()
        print('Golden Eagle Menu \n ------------ \n[1] Golden Eagle Scrape \n[2] Godlen Eagle From File'
              '\n[back] Back to Main Menu \n[exit] Exit Program')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            self.golden_eagle_scrape_menu()
        elif user_selection == '2':
            self.golden_eagle_from_file_menu()
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.golden_eagle_menu()
        self.golden_eagle_menu()

    def golden_eagle_scrape_menu(self):
        self.cls()
        print('Golden Eagle Scrape Menu \n ------------ \n[1] Echo \n[2] Billygoat \n[3] Both '
              '\n[back] Back to Previous Menu \n[exit] Exit Program')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
            ech.write_inventory()
        elif user_selection == '2':
            bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
            bil.write_inventory()
        elif user_selection == '3':
            ech = Distributor_Golden_Eagle.Golden_Eagle('ECH')
            bil = Distributor_Golden_Eagle.Golden_Eagle('BIL')
            ech.write_inventory()
            bil.write_inventory()
        elif user_selection == 'back':
            self.golden_eagle_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.golden_eagle_scrape_menu()
        self.golden_eagle_scrape_menu()

    def golden_eagle_from_file_menu(self):
        self.cls()
        print('Golden Eagle From File Menu \n ------------ \n[1] Echo\n[2] Billygoat \n[3] Both '
              '\n[back] Back to Previous Menu \n[exit] Exit Program')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            ech = From_File_Golden_Eagle.GoldenEagleFromFile('ECH')
            ech.write_inventory()
        elif user_selection == '2':
            bil = From_File_Golden_Eagle.GoldenEagleFromFile('BIL')
            bil.write_inventory()
        elif user_selection == '3':
            ech = From_File_Golden_Eagle.GoldenEagleFromFile('ECH')
            bil = From_File_Golden_Eagle.GoldenEagleFromFile('BIL')
            ech.write_to_filepath = 'T:/ebay/Golden Eagle/inventory/GoldenEagle_Scrape' +\
                                    time.strftime("%m%d" + '.' + "%I%M") + '.csv'
            bil.write_to_filepath = 'T:/ebay/Golden Eagle/inventory/GoldenEagle_Scrape' +\
                                    time.strftime("%m%d" + '.' + "%I%M") + '.csv'
            ech.write_inventory()
            bil.write_inventory()
        elif user_selection == 'back':
            self.golden_eagle_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.golden_eagle_from_file_menu()
        self.golden_eagle_from_file_menu()

    def cpd_xml_response(self):
        self.cls()
        print('CPD XML Response Menu \n ------------ \n[1] Kohler \n[2] Tecumseh \n[3] Hydro Gear \n[4] Case '
              '\n[5] AYP [6] NGK \n[7] All \n[back] Back to CPD Menu \n[exit] Exit Program')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            koh = XML_CPD.CPD('KOH')
            koh.get_xml_response()
        elif user_selection == '2':
            tec = XML_CPD.CPD('TEC')
            tec.get_xml_response()
        elif user_selection == '3':
            hyg = XML_CPD.CPD('HYD')
            hyg.get_xml_response()
        elif user_selection == '4':
            ic = XML_CPD.CPD('IC')
            ic.get_xml_response()
        elif user_selection == '5':
            ayp = XML_CPD.CPD('AYP')
            ayp.get_xml_response()
        elif user_selection == '6':
            ngk = XML_CPD.CPD('NGK')
            ngk.get_xml_response()
        elif user_selection == '7':
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
            try:
                ayp = XML_CPD.CPD('AYP')
                ayp.get_xml_response()
            except:
                pass
            try:
                ngk = XML_CPD.CPD('NGK')
                ngk.get_xml_response()
            except:
                pass
        elif user_selection == 'back':
            self.cpd_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.cpd_xml_response()
        self.cpd_xml_response()

    def cpd_xml_menu(self):
        self.cls()
        print('CPD XML Quantity Menu \n ------------ \n[1] Kohler \n[2] Tecumseh \n[3] Hydro Gear \n[4] Case \n[5] AYP '
              '\n[6] Martin Wheels \n[7] NGK \n[8] All \n[back] Back to CPD Menu \n[exit] Exit Program\n')
        user_selection = input('What would you like to do?: ')
        if user_selection == '1':
            koh = XML_CPD.CPD('KOH')
            koh.write_inventory()
        elif user_selection == '2':
            tec = XML_CPD.CPD('TEC')
            tec.write_inventory()
        elif user_selection == '3':
            hyg = XML_CPD.CPD('HYD')
            hyg.write_inventory()
        elif user_selection == '4':
            ic = XML_CPD.CPD('IC')
            ic.write_inventory()
        elif user_selection == '5':
            ayp = XML_CPD.CPD('AYP')
            ayp.write_inventory()
        elif user_selection == '6':
            mart = XML_CPD.CPD('MART')
            mart.write_inventory()
        elif user_selection == '7':
            ngk = XML_CPD.CPD('NGK')
            ngk.write_inventory()
        elif user_selection == '8':
            try:
                koh = XML_CPD.CPD('KOH')
                koh.write_inventory()
            except:
                pass
            try:
                tec = XML_CPD.CPD('TEC')
                tec.write_inventory()
            except:
                pass
            try:
                hyg = XML_CPD.CPD('HYD')
                hyg.write_inventory()
            except:
                pass
            try:
                case = XML_CPD.CPD('IC')
                case.write_inventory()
            except:
                pass
            try:
                ayp = XML_CPD.CPD('AYP')
                ayp.write_inventory()
            except:
                pass
            try:
                mart = XML_CPD.CPD('MART')
                mart.write_inventory()
            except:
                pass
            try:
                ngk = XML_CPD.CPD('NGK')
                ngk.write_inventory()
            except:
                pass
        elif user_selection == 'back':
            self.main_menu()
        elif user_selection == 'exit':
            sys.exit()
        else:
            print('That is not a valid selection please choose from the available options')
            self.cpd_xml_menu()
        self.cpd_xml_menu()

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')


program = UserInterface()
program.main_menu()
