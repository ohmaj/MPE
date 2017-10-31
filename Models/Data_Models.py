
class ResultsForEbay:

    def __init__(self, row):
        self.itemID = row[1]
        self.externalItemID = row[2]
        self.sku = row[3]
        self.productID = row[4].rstrip()
        self.storageLocation = row[5]
        self.quantity = row[6]
        self.cost = row[7]
        self.supplierID = row[8]
        self.supplierAccountNum = row[9]
        self.supplierName = row[10]
        self.datePurchased = row[11]
        self.fulfillmentSource = "Drop Shipper"
        self.poNumber = row[13]
        self.invoiceNumber = row[14]
        self.action = "Reconcileto"
        self.title = [16]
        self.msrp = [17]
        self.description = ''
        self.header_row_new_listings = ["Title","Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action","Description","MSRP"]
        self.header_row = ["Item ID","External Item ID","SKU","Product ID","Storage Location","Quantity","Cost","Supplier ID","Supplier Account Num","Supplier Name","Date Purchased","Fulfillment Source","PO Number","Invoice Number","Action","Description"]
        self.frameAsList = []

    def getFrameAsList(self):
        self.frameAsList = [self.itemID, self.externalItemID, self.sku, self.productID, self.storageLocation, self.quantity,
         self.cost, self.supplierID, self.supplierAccountNum, self.supplierName, self.datePurchased,
         self.fulfillmentSource, self.poNumber, self.invoiceNumber, self.action, self.description]

    def getFrameAsList_new_listing(self):
        self.frameAsList = [self.title, self.itemID, self.externalItemID, self.sku, self.productID, self.storageLocation, self.quantity,
         self.cost, self.supplierID, self.supplierAccountNum, self.supplierName, self.datePurchased,
         self.fulfillmentSource, self.poNumber, self.invoiceNumber, self.action, self.description, self.msrp]

class Ebay_Listing:

    def __init__(self):
        self.product_id1 = ''
        self.sku = ''
        self.product_id2 = ''
        self.item_id = ''
        self.ps_desc = ''
        self.title = ''
        self.product_brand = ''
        self.status = ''
        self.product_id_type = ''
        self.eBay_shipping_preset_name = ''
        self.weight_Major = ''
        self.weight_price_file = ''
        self.weight_minor = ''
        self.dimension_length = ''
        self.dimension_width = ''
        self.dimension_depth = ''
        self.is_taxable = ''
        self.qty_on_hand = ''
        self.qty_currently_listed = ''
        self.qty_to_List = ''
        self.cost = ''
        self.blank1 = ''
        self.blank2 = ''
        self.dis_code = ''
        self.msrp = ''
        self.fixed_price = ''
        self.profit = ''
        self.fees = ''
        self.eBay_title = ''
        self.eBay_condition = ''
        self.eBay_description_wrapper_name = ''
        self.eBay_description = ''
        self.eBay_payment_preset_name = ''
        self.eBay_private = ''
        self.eBay_category1ID = ''
        self.eBay_store_category1_name = ''
        self.eBay_store_category2_name = ''
        self.eBay_allocation_plane_name = ''
        self.is_type = ''
        self.is_brand = ''
        self.is_mpn = ''
        self.is_model = ''
        self.is_upc = ''
        self.picture = ''
        self.pre_img = ''
        self.as_list = ''
        self.header_row = ['Product ID', 'SKU', 'Product ID', 'Item ID', 'PS DESC', 'Title', 'Product Brand', 'Status', 'Product ID type', 'eBay Shipping Preset Name', 'Weight Major', 'Weight price file', 'weight minor',
                          'Dimension Length', 'Dimension Width', 'Dimension Depth', 'Is Taxable', 'Qty On Hand', 'Qty Currently Listed', 'Qty to List', 'Cost','','','dis - code', 'MSRP', 'fixed price', 'Profit', 'Fees',
                          'eBay Title', 'eBay Condition', 'eBay Description Wrapper Name', 'eBay Description', 'eBay Payment Preset Name', 'eBay Private', 'eBay Category1ID', 'eBay Store Category1Name',
                          'eBay Store Category2Name', 'eBay Allocation Plane Name', 'IS_Type', 'IS_Brand', 'IS_MPN', 'IS_Model', 'IS_UPC', 'PICTURE', 'PRE IMG']

    def get_list(self):
        self.as_list = [self.product_id1, self.sku, self.product_id2, self.item_id, self.ps_desc, self.title, self.product_brand,
                        self.status, self.product_id_type, self.eBay_shipping_preset_name, self.weight_Major, self.weight_price_file,
                        self.weight_minor, self.dimension_length, self.dimension_width, self.dimension_depth, self.is_taxable,
                        self.qty_on_hand, self.qty_currently_listed, self.qty_to_List, self.cost, self.blank1, self.blank2,
                        self.dis_code, self.msrp, self.fixed_price, self.profit, self.fees, self.eBay_title, self.eBay_condition,
                        self.eBay_description_wrapper_name, self.eBay_description, self.eBay_payment_preset_name, self.eBay_private,
                        self.eBay_category1ID, self.eBay_store_category1_name, self.eBay_store_category2_name, self.eBay_allocation_plane_name,
                        self.is_type, self.is_brand, self.is_mpn, self.is_model, self.is_upc, self.picture, self.pre_img, self.as_list]

class AIP_Scrape:

    def __init__(self):
        self.graphics = []
        self.product_attributes = []
        self.megaCross = []
        self.kitDetails = []
        self.kitMaster = []
        self.models = []
        self.weight = []
        self.retailer_price = []
        self.list = []
        self.fancy_list = []

    def get_fancy_list(self):
        temp_list = []
        if self.graphics:
            temp_list.append(['graphic links', self.graphics])
        if self.product_attributes:
            temp_list.append(['Attributes', self.product_attributes])
        if self.megaCross:
            temp_list.append(['Mega Cross',self.megaCross])
        if self.kitDetails:
            temp_list.append(['Included in this kit',self.kitDetails])
        if self.kitMaster:
            temp_list.append(['This item is in these kits',self.kitMaster])
        if self.models:
            temp_list.append(['For Models',self.models])
        if self.weight:
            temp_list.append(['Product Weight',self.weight])
        if self.retailer_price:
            temp_list.append(['Retailer Price',self.retailer_price])
        self.fancy_list = temp_list

    def get_list(self):
        self.list = [self.expand_all(self.graphics), self.expand_all([self.expand_all(self.product_attributes), self.expand_all(self.megaCross), self.expand_all(self.kitDetails),
         self.expand_all(self.kitMaster), self.expand_all(self.models)]), self.expand_all(self.weight)]

    def expand_all(self, input_list):
        temp_list = []
        if input_list:
            for field in input_list:
                if type(field) is list:
                    temp_list.append(self.expand_all(field))
                elif type(field) is None:
                    continue
                else:
                    if field == None:
                        continue
                    else:
                        temp_list.append(field)
        return(' '.join(temp_list))

class CPD_Inquiry:
    def __init__(self, row):
        self.customer_number = '22462'
        self.manufacturer_code = row[2]
        self.part_number = row[3]
        self.quantity = '20'