from classes import ABC_Distributor
from abc import abstractmethod
import time


class DistributorApiXml(ABC_Distributor.Distributor):

    def __init__(self, mfr):
        super(DistributorApiXml, self).__init__(mfr)
        self.mfr = mfr
        self.errors_filepath = r'T:/ebay/' + mfr + '/inventory/' + mfr + '_API_'

    def write_api_files(self, inquiry, response, i):
        # ---------------- write inquiry to file for error checking--------------
        file_path = self.errors_filepath + self.mfr + '_Api_Inquiry' + str(i) + '.xml'
        temp_writer = open(file_path, 'w')
        temp_writer.write(inquiry)
        temp_writer.close()
        # -----------------write response to file for error checking---------------
        file_path = self.errors_filepath + self.mfr + '_Api_Response' + str(i) + '.xml'
        temp_writer = open(file_path, 'w')
        temp_writer.write(response.text)
        temp_writer.close()

    @abstractmethod
    def get_xml(self, products):
        pass

    @abstractmethod
    def get_cpd_response(self, xml_inquiry):
        pass

    @abstractmethod
    def parse_xml_response_for_ebay_listing(self, xml_file):
        pass

    def get_distributor_inventory_dictionary(self):
        product_ids = self.get_product_dictionary()
        xml_inquiry = self.get_xml(product_ids)
        responses = self.get_cpd_response(xml_inquiry)
        distributor_inventory = self.parse_xml_response_for_ebay_listing(responses)
        return distributor_inventory
