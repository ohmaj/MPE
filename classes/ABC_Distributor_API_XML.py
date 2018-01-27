from classes import ABC_Distributor
import time
import csv
import requests


class DistributorApiXml(ABC_Distributor.Distributor):

    def __init__(self, mfr):
        super(DistributorApiXml, self).__init__(mfr)
        self.mfr = mfr
        self.errors_filepath = r'T:/ebay/' + mfr + '/inventory/' + mfr + '_API_' + time.strftime(
            '%m%d%Y' + '_' + '%I%M') + '.csv'
        self.end_point_url = "http://2cpdonline.com/mh/inquiry.asp"
        self.product_data_set = self.get_data_set()

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

    def get_xml_response(self):
        i = 1
        xml_inquiries = list(self.get_xml())
        count = len(xml_inquiries)
        for inquiry in xml_inquiries:
            print(self.mfr + ' Getting Response: ' + str(i) + ' of ' + str(count))
            response = self.get_response(inquiry)
            file_path = self.errors_filepath + self.mfr + '_Api_Response' + str(i) + '.xml'
            temp_writer = open(file_path, 'w')
            temp_writer.write(response.text)
            temp_writer.close()
            i += 1

    def get_xml(self):
        data_set = list(self.product_data_set)
        count = 0
        data_set_count = len(data_set)
        while count < data_set_count:
            i = 0
            xml_request = self.xml_header
            while i < self.inquiry_limit and count < data_set_count:
                xml_data_point = self.get_xml_datapoint(data_set[count])
                xml_request = xml_request+xml_data_point
                i += 1
                count += 1
                self.cls()
                print(self.mfr+' Making Inquiry: ' + str(int((count/data_set_count)*100))+'%')
            xml_request = xml_request+self.xml_footer
            # noinspection PyUnusedLocal
            i = 0
            yield xml_request

    def get_data_set(self):
        with open(self.product_ids_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield (row)

    def get_cpd_response(self, xml_request):
        # headers = {'Content-Type': 'application/xml'}
        response = requests.post(self.end_point_url, data=xml_request)
        return response
