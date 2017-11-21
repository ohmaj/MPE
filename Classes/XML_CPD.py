import os
import time
import csv
import requests
from lxml import etree as element_tree
from Models import Data_Models
import codecs

class CPD:

    def __init__(self, mfr):
        self.mfr = mfr
        self.product_ids_filepath = r'T:/ebay/'+mfr+'/inventory/ProductIds.csv'
        self.save_to_filepath = r'T:/ebay/'+mfr+'/inventory/'+self.mfr+'_API_'+time.strftime('%m%d%Y'+'_'+'%I%M')+'.csv'
        self.errors_filepath = r'T:/ebay/'+mfr+'/inventory/'+self.mfr+'_API_'+time.strftime('%m%d%Y'+'_'+'%I%M')+'.csv'
        self.end_point_url = "http://2cpdonline.com/mh/inquiry.asp"
        self.product_data_set = self.get_data_set()
        self.xml_header = '<?xml version="1.0" encoding="utf-8" ?><inventory_request>\n'
        self.xml_footer = '</inventory_request>'
        self.inquiry_limit = 1000

    def write_inventory(self):
        xml_inquiries = list(self.get_xml())
        parsed_data_set = []
        i = 1
        count = len(xml_inquiries)
        for inquiry in xml_inquiries:
            print(self.mfr + ' Getting Response: ' + str(i) + ' of ' + str(count))
            try:
                response = self.get_cpd_response(inquiry)
            except:
                self.write_api_files(inquiry, response)
            try:
                parsed_data_points = list(self.parse_xml_response_for_ebay_listing(response))
                for point in parsed_data_points:
                    parsed_data_set.append(point)
            except:
                pass
            i += 1
        self.write_data_set_to_csv(parsed_data_set)

    def get_inventory(self):
        xml_inquiries = list(self.get_xml())
        parsed_data_set = []
        i = 1
        count = len(xml_inquiries)
        for inquiry in xml_inquiries:
            print(self.mfr + ' Getting Response: ' + str(i) + ' of ' + str(count))
            try:
                response = self.get_cpd_response(inquiry)
            except:
                self.write_api_files(inquiry, response)
            try:
                parsed_data_points = list(self.parse_xml_response_for_ebay_listing(response))
                for point in parsed_data_points:
                    parsed_data_set.append(point)
            except:
                pass
            i += 1
        return(parsed_data_set)

    def write_api_files(self, inquiry, response):
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

    def get_xml_response(self):
        i = 1
        xml_inquiries = list(self.get_xml())
        count = len(xml_inquiries)
        for inquiry in xml_inquiries:
            print(self.mfr + ' Getting Response: ' + str(i) + ' of ' + str(count))
            response = self.get_cpd_response(inquiry)
            file_path = self.errors_filepath + self.mfr + '_Api_Response' +str(i)+ '.xml'
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

    def get_xml(self):
        data_set = list(self.product_data_set)
        count = 0
        data_set_count = len(data_set)
        while count < (data_set_count):
            i = 0
            xml_request = self.xml_header
            while i < self.inquiry_limit and count < (data_set_count):
                xml_dataPoint = self.get_xml_datapoint(data_set[count])
                xml_request = xml_request+xml_dataPoint
                i += 1
                count += 1
                self.cls()
                print(self.mfr+' Making Inquiry: '+ str(int((count/data_set_count)*100))+'%')
            xml_request = xml_request+self.xml_footer
            i = 0
            yield xml_request

    def get_cpd_response(self, xml_request):
        # headers = {'Content-Type': 'application/xml'}
        response = requests.post(self.end_point_url, data = xml_request)
        return (response)

    def parse_xml_response_for_ebay_listing(self, xml_file):
        parser = element_tree.XMLParser(recover=True)
        tree = element_tree.fromstring(xml_file.content, parser=parser)
        i = 1
        for part in tree:
            try:
                itemID = self.none_clean(part.findall('CustomerInternalSKU')[0].text)
                productID = self.none_clean(part.findall('PartNumberInquired')[0].text)
                sku = '['+self.mfr+']['+productID+']'
                cost = self.none_clean(part.findall('UnitPrice')[0].text)
                quantity = self.none_clean(part.findall('QuantityAvailable')[0].text)
                supplierAccountNum = '22462'
                supplierID = '8'
                supplierName = 'Amanda  Fitzerold'
                data_point = Data_Models.ResultsForEbay(['', itemID, '', sku, productID, '', quantity, cost, supplierID, supplierAccountNum, supplierName, '', 'Drop Shipper', '', '', 'Reconcileto', '', ''])
                data_point.getFrameAsList()
                if data_point.frameAsList[5] == '':
                    data_point.frameAsList[5] = 'error'
                yield data_point
            except Exception as inst:
                data_point = Data_Models.ResultsForEbay(
                    ['', '', '', '', '', 'Error', '', '', '', '', '', '', '', '', '', '',inst.__str__()])
                data_point.getFrameAsList()
                yield (data_point)
            i +=1

    def parse_xml_response_for_new_listing(self, xml_file):
        parser = element_tree.XMLParser(recover=True)
        tree = element_tree.fromstring(xml_file.content, parser=parser)
        i = 1
        for part in tree:
            try:
                title = self.none_clean((part.findall('PartDescription'))[0].text)
                msrp = self.none_clean(part.findall('RetailPrice')[0].text)
                productID = self.none_clean(part.findall('PartNumberInquired')[0].text)
                sku = '['+self.mfr+']['+productID+']'
                cost = self.none_clean(part.findall('UnitPrice')[0].text)
                quantity = self.none_clean(part.findall('QuantityAvailable')[0].text)
                supplierAccountNum = '22462'
                supplierID = '8'
                supplierName = 'Amanda  Fitzerold'
                data_point = Data_Models.ResultsForEbay(['', '', sku, productID, '', quantity, cost, supplierID, supplierAccountNum, supplierName, '', '', '', '', 'Reconcileto', title, msrp])
                data_point.getFrameAsList_new_listing()
                yield (data_point)
            except:
                pass
            i +=1

    def get_xml_datapoint(self, data_point):
        mfr = self.mfr
        if mfr == 'MART':
            mfr = 'MAR'
        smart_order = ('<SmartOrder><CustomerNumber>'+data_point['Supplier ID']+'</CustomerNumber><ManufacturerCode>'+mfr+'</ManufacturerCode><PartNumber>'+data_point['Product ID']+'</PartNumber><Quantity>10</Quantity><ClientNoSupNLA/><UPCCode/><InquirySequenceNumber/><CustomerInternalSKU>'+data_point['Item ID']+'</CustomerInternalSKU></SmartOrder>')
        return(smart_order)

    def write_data_set_to_csv(self, data_set):
        ordered_dicts = [{'Item ID': product.frameAsList[0],
                          'External Item ID': product.frameAsList[1],
                          'SKU': product.frameAsList[2],
                          'Product ID': product.frameAsList[3],
                          'Storage Location': product.frameAsList[4],
                          'Quantity': product.frameAsList[5],
                          'Cost': product.frameAsList[6],
                          'Supplier ID': product.frameAsList[7],
                          'Supplier Account Num': product.frameAsList[8],
                          'Supplier Name': product.frameAsList[9],
                          'Date Purchased': product.frameAsList[10],
                          'Fulfillment Source': product.frameAsList[11],
                          'PO Number': product.frameAsList[12],
                          'Invoice Number': product.frameAsList[13],
                          'Action': product.frameAsList[14]
                          } for product in data_set]
        keys = ordered_dicts[0].keys()
        with open(self.save_to_filepath, 'a', newline='', encoding="latin-1") as csv_file:
            dict_writer = csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(ordered_dicts)

    def get_data_set(self):
        with open(self.product_ids_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield (row)

    def none_clean(self, input):
        return(str(input).replace('None', ''))

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
