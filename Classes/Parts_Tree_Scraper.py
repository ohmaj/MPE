from lxml import html
import requests
from Models import Parts_Tree_Model
import csv
import time
import os

class Parts_Tree_Scraper:

    def __init__(self):
        self.product_ids_filepath = r'T:\ebay\AYP\Temp New Listings\ProductIds.csv' #product_ids_filepath
        self.results_filepath = r'T:\ebay\AYP\Temp New Listings\Parts_Tree' + time.strftime("%m%d%Y"+'.'+"%I%M") + '.csv'

    def run(self):
        data_set = list(self.get_data_set())
        scraped_dataset = list(self.run_scrape(data_set))
        self.write_list_to_file(scraped_dataset)

    def write_list_to_file(self, list):
        with open(self.results_filepath, 'w', newline='') as csv_file:
            wr = csv.writer(csv_file, delimiter=',')
            wr.writerow(list[0].header_row)
            for item in list:
                try:
                    item.get_as_list()
                    wr.writerow(item.as_list)
                except:
                    pass

    def run_scrape(self, data_set):
        count = 1
        total = len(list(data_set))
        for part in data_set:
            # construct url
            url = self.construct_url(part['MFR'], ((part['Product ID']).strip('[]').replace(' ','-')))
            # scrape url
            parts_tree_part = self.scrape_part(url)
            self.cls()
            print('Scrape Progress: ' + str(int((count / total) * 100)) + '%')
            count += 1
            parts_tree_part.part_id = part['Product ID']
            parts_tree_part.part_id = parts_tree_part.part_id
            parts_tree_part.item_id = part['Item ID']
            yield (parts_tree_part)

    def construct_url(self, mfr, id):
        return ('http://www.partstree.com/parts/'+mfr+'/parts/'+id+'/')

    def scrape_part(self, url):
        page = requests.get(url)
        tree = html.fromstring(page.content)
        parts_tree_part = Parts_Tree_Model.Parts_Tree_Model()
        try:
            parts_tree_part.part_id = tree.xpath('/html/body/div[2]/div[2]/div[5]/div/div[2]/p[1]/span[2]/text()')[0]
        except:
            pass
        try:
            parts_tree_part.part_description = tree.xpath('/html/body/div[2]/div[2]/div[5]/div/div[2]/p[3]/text()')[0]
        except:
            pass
        try:
            compatable_machines = tree.xpath('/html/body/div[2]/div[2]/div[6]/ul/li/a/text()')
            parts_tree_part.compatable_machines = '<br>'.join(compatable_machines)
        except:
            pass
        try:
            parts_tree_part.part_thumbnail_src = tree.xpath('/html/body/div[2]/div[2]/div[4]/div[2]/div[1]/a/img/@src')[0]
        except:
            pass
        return (parts_tree_part)

    def get_data_set(self):
        with open(self.product_ids_filepath, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield (row)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')