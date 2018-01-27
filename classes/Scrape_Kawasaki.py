from classes import ABC_Distributor_Scrape
from lxml import html


class Kawasaki(ABC_Distributor_Scrape.DistributorScrape):

    def __init__(self, manufacturer):
        super(Kawasaki, self).__init__(manufacturer)

    def load_product(self, product_id, browser):
        product_search_url = 'https://kawasakipower.com/ProductDetail?DealerID=51948&UserID=kmc51948&' \
                           'SessionID=550577559254125&ProductID='
        browser.get(product_search_url + product_id + '&ProductQlfr=KWE')

    def parse_scrape(self, item, html_scrape):
        tree = html.fromstring(html_scrape)
        availability_imgs = tree.xpath('//*[@id="product-detail"]/tbody/tr[5]//img/@src')
        # cost = tree.xpath('//*[@id="product-detail"]/tbody/tr[2]/td[2]/text()')
        availability = '0'
        if len(availability_imgs) > 0:
            for src in availability_imgs:
                if src == '/img/legend/diamond-green-1.gif':
                    availability = '10'
                    break
        # TODO needs work to get kawasaki cost correctly
        # item['Cost'] = cost[0].strip('$ ')
        item['Quantity'] = availability
        return item

    def login(self):
        pass
