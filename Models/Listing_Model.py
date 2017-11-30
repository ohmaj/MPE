

class Create_Ebay_Listing:

    def __init__(self):
        self.sku = ''
        self.product_id = ''
        self.product_id_type = 'NONE'
        self.product_brand = ''
        self.product_mfr = ''
        self.raw_title = ''
        self.title = ''
        self.weight_pricefile = ''
        self.weight_major = ''
        self.weight_minor = ''
        self.cost = ''
        self.fees = ''
        self.profit = ''
        self.fixed_price = ''
        self.msrp = ''
        self.lot_size = '1'
        self.ebay_category1_id = '82248'
        self.primary_fullfillment = 'Self'
        self.secondary_fullfillment = 'Drop Shipper'
        self.is_brand = ''
        self.is_mpn = ''
        self.is_model = ''
        self.is_item_condition = 'New'
        self.ebay_payment_preset_name = ''
        self.ebay_preset_wrapper_name = ''
        self.ebay_description_wrapper_name = ''
        self.where_used = ''
        self.ebay_shipping_preset_name = ''
        self.picture_url = ''
        self.ebay_description = ''

    def set_title(self):
        self.title = 'Genuine ' + self.product_brand+' Part ' + self.raw_title + ' ' + self.sku

    def set_sku(self):
        self.sku = '[' + self.product_mfr + '][' + self.product_id + ']'
        self.is_mpn = self.sku
        self.is_model = self.sku

    def set_where_used_html(self):
        if self.where_used == '':
            self.ebay_description = '<span style="font-size: 16pt; color: #ef0f0f">Commonly Used on Models:<br /><br /> More Information Coming Soon' + self.where_used
        else:
            self.ebay_description = '<span style="font-size: 16pt; color: #ef0f0f">Commonly Used on Models:<br /><br />' + self.where_used

    def get_part_as_dict(self):
        part = {}
        part['SKU'] = self.sku
        part['Product ID'] = self.product_id
        part['Product ID Type'] = self.product_id_type
        part['Product Brand'] = self.product_brand
        part['Title'] = self.title
        part['Weight Price File'] = self.weight_pricefile
        part['Weight Major'] = self.weight_major
        part['Weight Minor'] = self.weight_minor
        part['Cost'] = self.cost
        part['Fees'] = self.fees
        part['Profit'] = self.profit
        part['Fixed Price'] = self.fixed_price
        part['MSRP'] = self.msrp
        part['Lot Size'] = self.lot_size
        part['eBay Category1ID'] = self.ebay_category1_id
        part['Primary Fulfillment Soruce'] = self.primary_fullfillment
        part['Secondary Fulfillment Source'] = self.secondary_fullfillment
        part['IS_Brand'] = self.is_brand
        part['IS_MPN'] = self.is_mpn
        part['IS_Item Condition'] = self.is_item_condition
        part['eBay Payment Preset Name'] = self.ebay_payment_preset_name
        part['eBay Preset Wrapper Name'] = self.ebay_preset_wrapper_name
        part['eBay Description Wrapper Name'] = self.ebay_description_wrapper_name
        part['ebay Shipping Preset Name'] = self.ebay_shipping_preset_name
        part['Picture'] = self.picture_url
        part['eBay Description'] = self.ebay_description
        return part

    def set_all(self):
        self.set_sku()
        self.set_title()
        self.set_where_used_html()
