from Classes import Distributor
from lxml import html


class AIP(Distributor.ScrapeDistributor):

    def __init__(self, manufacturer):
        super(AIP, self).__init__(manufacturer)

    def login(self, browser):
        login_url = r'https://' + self.username + ':' + self.password + '@www.aiproducts.com/dealer/customer.htm'
        browser.get(login_url)
        frame_x_path = '/html/frameset/frameset/frame[1]'
        menu_x_path = '/html/body/a[2]/p'
        sub_menu_x_path = '//*[@id="sub1"]/a[2]'
        frame = browser.find_element_by_xpath(frame_x_path)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(menu_x_path).click()
        browser.find_element_by_xpath(sub_menu_x_path).click()

    def load_product(self, product_id, browser):
        browser.switch_to.default_content()
        frame_xpath = r'/html/frameset/frameset/frame[2]'
        item_number_input_xpath = r'//html/body/form/table/tbody/tr/td[1]/table/tbody/tr[1]/td[3]/input'
        qty_input_xpath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[1]'
        check_button_xpath = r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[2]/td[3]/input[2]'
        frame = browser.find_element_by_xpath(frame_xpath)
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath(item_number_input_xpath).clear()
        browser.find_element_by_xpath(item_number_input_xpath).send_keys(product_id.strip('[]'))
        browser.find_element_by_xpath(qty_input_xpath).clear()
        browser.find_element_by_xpath(qty_input_xpath).send_keys('10')
        browser.find_element_by_xpath(check_button_xpath).click()

    def parse_scrape(self, item, html_scrape):
        tree = html.fromstring(html_scrape)
        adjust_t_r = 0
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[10]/td/img'):
            adjust_t_r = 1
        if (tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[14]/td[1]/text()')[0]) == ':':
            item['Quantity'] = 'invalid'
            return item
        if tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[11]/td/table/tbody/tr[2]/td[2]/input'):
            item['Quantity'] = 'vendor dropship'
            return item
        ia = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 10) + ']/td[3]/text()')[0])
        ind = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                             str(adjust_t_r + 11) + ']/td[3]/text()')[0])
        mo = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 12) + ']/td[3]/text()')[0])
        nc = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 13) + ']/td[3]/text()')[0])
        tx = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 14) + ']/td[3]/text()')[0])
        ca = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 15) + ']/td[3]/text()')[0])
        wa = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 16) + ']/td[3]/text()')[0])
        pa = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 17) + ']/td[3]/text()')[0])
        ga = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 18) + ']/td[3]/text()')[0])
        fl = int(tree.xpath(r'/html/body/form/table/tbody/tr/td[1]/table/tbody/tr[' +
                            str(adjust_t_r + 19) + ']/td[3]/text()')[0])
        qty = ia + ind + mo + nc + tx + ca + wa + pa + ga + fl
        item['Quantity'] = qty
        return item
