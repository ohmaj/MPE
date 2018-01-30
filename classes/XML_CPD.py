from classes import ABC_Distributor_API_XML
import time
from lxml import etree as element_tree
import requests


class CPD(ABC_Distributor_API_XML.DistributorApiXml):

    def __init__(self, mfr):
        super(CPD, self).__init__(mfr)
        self.mfr = mfr
        self.product_ids_filepath = r'T:/ebay/'+mfr+'/inventory/ProductIds.csv'
        self.save_to_filepath = r'T:/ebay/'+mfr+'/inventory/'+self.mfr+'_API_'+time.strftime('%m%d%Y'+'_'+'%I%M')+'.csv'
        self.end_point_url = "http://2cpdonline.com/mh/inquiry.asp"
        self.xml_header = '<?xml version="1.0" encoding="utf-8" ?><inventory_request>'
        self.xml_footer = '</inventory_request>'
        self.inquiry_limit = 3000

    def get_xml(self, produts):
        data_set = produts.items()
        xml_request = self.xml_header
        count = 0
        for k, v in data_set:
            if count >= self.inquiry_limit:
                count = 1
                new_xml_request = xml_request + self.xml_footer
                xml_request = self.xml_header
                xml_data_point = self.get_xml_datapoint(v)
                xml_request = xml_request + xml_data_point
                yield new_xml_request
            xml_data_point = self.get_xml_datapoint(v)
            xml_request = xml_request+xml_data_point
            count += 1
        xml_request = xml_request+self.xml_footer
        yield xml_request

    def get_cpd_response(self, xml_requests):
        for xml_request in list(xml_requests):
            response = requests.post(self.end_point_url, data=xml_request)
            file_path = self.errors_filepath + self.mfr + '_Api_REPLY' + '.xml'
            temp_writer = open(file_path, 'w')
            temp_writer.write(response.text)
            yield response

    def parse_xml_response_for_ebay_listing(self, responses):
        distributor_inventory_dict = {}
        for response in responses:
            parser = element_tree.XMLParser(recover=True)
            reader = element_tree.fromstring(response.content, parser=parser)
            i = 1
            for row in reader:
                part = {}
                try:
                    part['Product ID'] = self.none_clean(row.findall('PartNumberInquired')[0].text)
                    part['Fulfillment Source'] = 'Drop Shipper'
                    part['Action'] = 'Reconcileto'
                    part['Error'] = ''
                    part['Qty on Hand'] = self.none_clean(row.findall('QuantityAvailable')[0].text)
                    if self.none_clean(row.findall('PartNumberInquired')[0].text) == '':
                        part['Qty on Hand'] = self.none_clean(row.findall('QuantityAvailable')[0].text)
                    distributor_inventory_dict[part['Product ID']] = part
                except Exception as inst:
                    part['Product ID'] = self.none_clean(row.findall('PartNumberInquired')[0].text)
                    part['Fulfillment Source'] = 'Drop Shipper'
                    part['Action'] = 'Reconcileto'
                    part['Error'] = inst.__str__()
                    part['Qty on Hand'] = 'Error'
                    distributor_inventory_dict[part['Product ID']] = part
                i += 1
        return distributor_inventory_dict

    def get_xml_datapoint(self, data_point):
        mfr = self.mfr
        if mfr == 'MART':
            mfr = 'MAR'
        smart_order = ('\n<SmartOrder><CustomerNumber></CustomerNumber><ManufacturerCode>' +
                       mfr + '</ManufacturerCode><PartNumber>'+data_point['Product ID'] +
                       '</PartNumber><Quantity>10</Quantity><ClientNoSupNLA/><UPCCode/><InquirySequenceNumber/>'
                       '<CustomerInternalSKU>' + data_point['Item ID'] + '</CustomerInternalSKU></SmartOrder>')
        return smart_order

    @staticmethod
    def none_clean(input_string):
        return str(input_string).replace('None', '')

    # def get_xml_response(self, xml_inquiry):
    #     i = 1
    #     xml_inquiries = list(xml_inquiry)
    #     count = len(xml_inquiries)
    #     for inquiry in xml_inquiries:
    #         print(self.mfr + ' Getting Response: ' + str(i) + ' of ' + str(count))
    #         response = self.get_cpd_response(inquiry)
    #         file_path = self.errors_filepath + self.mfr + '_Api_Response' + str(i) + '.xml'
    #         temp_writer = open(file_path, 'w')
    #         temp_writer.write(response.text)
    #         temp_writer.close()
    #         i += 1
