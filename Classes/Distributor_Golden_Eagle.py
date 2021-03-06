from Classes import Distributor
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Golden_Eagle(Distributor.ScrapeDistributor):

    def __init__(self, manufacturer):
        super(Golden_Eagle, self).__init__(manufacturer)
        self.login_url = r'http://netstore.goldeneagledist.com/netstore/StartServlet'
        self.product_search_url = r'http://netstore.goldeneagledist.com/netstore/ItemDetailServlet?KEY_ITEM='

    def login(self, browser):
        # logon_dict = User_Info.Credentials('Golden_Eagle')
        username_name = 'User'
        password_name = 'Password'
        login_button_name = 'ACTION_SIGNON'
        login_button_xpath = '//*[@id="layout-middle"]/div/div[1]/div[1]/ul/li[1]/a'
        browser.get(self.login_url)
        myElem = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, login_button_xpath)))
        browser.find_element_by_xpath(login_button_xpath).click()
        browser.find_element_by_name(username_name).clear()
        browser.find_element_by_name(username_name).send_keys(self.username)
        browser.find_element_by_name(password_name).send_keys(self.password)
        browser.find_element_by_name(login_button_name).click()

    def load_product(self, product_id, browser):
        if browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a/text()') == 'Sign on':
            self.login()
        productSearchUrl = self.product_search_url
        browser.get(productSearchUrl+self.manufacturer+'++'+product_id)

    def parse_scrape(self, item, htmlScrape):
        tree = html.fromstring(htmlScrape)
        description = ''
        availabilityImg = tree.xpath(
            '//*[@id="ItemDetailForm"]/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td[2]//@src')
        availability = '0'
        if len(availabilityImg) < 1:
            availability = 'Skipped'
        elif availabilityImg[0] == '/netstore/IBSStaticResources/NS_Resources/Available.gif':
            availability = '10'
        try:
            description = tree.xpath('//*[@id="ItemThumbnails"]/div/text()')[0]
        except:
            pass
        item['Quantity'] = availability
        item['Description'] = description
        return item
