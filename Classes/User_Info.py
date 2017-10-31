import base64
import json
import csv
import ast

class Credentials:
    def __init__(self, distributor):
        self.distributor = distributor
        self.file = 'T:\ebay\All\Logon_Info.csv'
        self.data_set = {}
        self.username = ''
        self.password = ''

    def get_account_credentials(self):
        with open(self.file, mode='r') as infile:
                reader = csv.reader(infile)
                self.data_set = {rows[0]: {'username' : rows[1], 'password' : rows[2]} for rows in reader}

    def set_logon_info(self):
        distributor = self.data_set[self.distributor]
        self.username = distributor['username']
        self.password = distributor['password']

    # def update_logon_info(self):
    #     with open(self.file, 'w') as json_file:
    #         credentials = {'username': self.username, 'password':self.password}
    #         self.data_set[self.distributor] = credentials

    def add_logon_info(self):
        self.data_set[self.distributor] = {'username':self.username, 'password':self.password}
        data_set_list = []
        for distributor, logon_info in self.data_set.items():
            credentials = [distributor]
            for k, v in logon_info.items():
                credentials.append(v)
            data_set_list.append(credentials)
        with open(self.file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data_set_list)