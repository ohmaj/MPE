from classes import ABC_Distributor_API_XML
import os
import time
import csv
from lxml import etree as element_tree
from models import Data_Models


class CPD(ABC_Distributor_API_XML):

    def __init__(self, mfr):
        super(CPD, self).__init__()
        self.mfr = mfr
        self.product_ids_filepath = r'T:/ebay/'+mfr+'/inventory/ProductIds.csv'
        self.save_to_filepath = r'T:/ebay/'+mfr+'/inventory/'+self.mfr+'_API_'+time.strftime('%m%d%Y'+'_'+'%I%M')+'.csv'

        self.xml_header = '<?xml version="1.0" encoding="utf-8" ?><inventory_request>\n'
        self.xml_footer = '</inventory_request>'
        self.inquiry_limit = 1000

    def get_xml_response(self):
        i = 1
        xml_inquiries = list(self.get_xml())
        count = len(xml_inquiries)
        for inquiry in xml_inquiries:
            print(self.mfr + ' Getting Response: ' + str(i) + ' of ' + str(count))
            response = self.get_cpd_response(inquiry)
            file_path = self.errors_filepath + self.mfr + '_Api_Response' + str(i) + '.xml'
            temp_writer = open(file_path, 'w')
            temp_writer.write(response.text)
            temp_writer.close()
            i += 1

    def get_new_listings(self):
        xml_inquiries = list(self.get_xml())
        parsed_data_set = []
        for inquiry in xml_inquiries:
            try:
                response = self.get_cpd_response(inquiry)
                parsed_data_points = list(self.parse_xml_response_for_new_listing(response))
                for point in parsed_data_points:
                    parsed_data_set.append(point)
                self.write_data_set_to_csv(parsed_data_set)
            except:
                pass

    def parse_xml_response_for_ebay_listing(self, xml_file):
        parser = element_tree.XMLParser(recover=True)
        tree = element_tree.fromstring(xml_file.content, parser=parser)
        i = 1
        for part in tree:
            try:
                item_id = self.none_clean(part.findall('CustomerInternalSKU')[0].text)
                product_id = self.none_clean(part.findall('PartNumberInquired')[0].text)
                sku = '[' + self.mfr + '][' + product_id + ']'
                cost = self.none_clean(part.findall('UnitPrice')[0].text)
                quantity = self.none_clean(part.findall('QuantityAvailable')[0].text)
                supplier_account_num = '22462'
                supplier_id = '8'
                supplie_name = 'Amanda  Fitzerold'
                data_point = Data_Models.ResultsForEbay(['', item_id, '', sku, product_id, '', quantity, cost,
                                                         supplier_id, supplier_account_num, supplie_name, '',
                                                         'Drop Shipper', '', '', 'Reconcileto', '', ''])
                data_point.get_frame_as_list()
                if data_point.frameAsList[5] == '':
                    data_point.frameAsList[5] = 'error'
                yield data_point
            except Exception as inst:
                data_point = Data_Models.ResultsForEbay(
                    ['', '', '', '', '', 'Error', '', '', '', '', '', '', '', '', '', '', inst.__str__()])
                data_point.get_frame_as_list()
                yield (data_point)
            i += 1

    def parse_xml_response_for_new_listing(self, xml_file):
        parser = element_tree.XMLParser(recover=True)
        tree = element_tree.fromstring(xml_file.content, parser=parser)
        i = 1
        for part in tree:
            try:
                title = self.none_clean((part.findall('PartDescription'))[0].text)
                msrp = self.none_clean(part.findall('RetailPrice')[0].text)
                product_id = self.none_clean(part.findall('PartNumberInquired')[0].text)
                sku = '['+self.mfr+']['+product_id+']'
                cost = self.none_clean(part.findall('UnitPrice')[0].text)
                quantity = self.none_clean(part.findall('QuantityAvailable')[0].text)
                supplier_account_num = '22462'
                supplier_id = '8'
                supplier_name = 'Amanda  Fitzerold'
                data_point = Data_Models.ResultsForEbay(['', '', sku, product_id, '', quantity, cost, supplier_id,
                                                         supplier_account_num, supplier_name, '', '', '', '',
                                                         'Reconcileto', title, msrp])
                data_point.get_frame_as_list_new_listing()
                yield (data_point)
            except:
                pass
            i += 1

    def get_xml_datapoint(self, data_point):
        mfr = self.mfr
        if mfr == 'MART':
            mfr = 'MAR'
        smart_order = ('<SmartOrder><CustomerNumber>'+data_point['Supplier ID']+'</CustomerNumber><ManufacturerCode>' +
                       mfr + '</ManufacturerCode><PartNumber>'+data_point['Product ID'] +
                       '</PartNumber><Quantity>10</Quantity><ClientNoSupNLA/><UPCCode/><InquirySequenceNumber/>'
                       '<CustomerInternalSKU>' + data_point['Item ID'] + '</CustomerInternalSKU></SmartOrder>')
        return smart_order

    def none_clean(self, input_string):
        return str(input_string).replace('None', '')

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
