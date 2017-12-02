

class CreateEbayListing:

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
        self.is_taxable = 'TRUE'
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
            self.ebay_description = '<span style="font-size: 16pt; color: #ef0f0f">Commonly Used on Models:<br />' \
                                    '<br /> More Information Coming Soon' + self.where_used
        else:
            self.ebay_description = '<span style="font-size: 16pt; color: #ef0f0f">' \
                                    'Commonly Used on Models:<br /><br />' + self.where_used

    def get_part_as_dict(self):
        part = {'SKU': self.sku,
                'Product ID': self.product_id,
                'Product ID Type': self.product_id_type,
                'Product Brand': self.product_brand,
                'Title': self.title,
                'Weight Price File': self.weight_pricefile,
                'Weight Major': self.weight_major,
                'Weight Minor': self.weight_minor,
                'Cost': self.cost,
                'Fees': self.fees,
                'Profit': self.profit,
                'Fixed Price': self.fixed_price,
                'MSRP': self.msrp,
                'eBay Lot Size': self.lot_size,
                'eBay Category1ID': self.ebay_category1_id,
                'Primary Fulfillment Soruce': self.primary_fullfillment,
                'Secondary Fulfillment Source': self.secondary_fullfillment,
                'IS_Brand': self.is_brand,
                'IS_MPN': self.is_mpn,
                'IS Taxable': self.is_taxable,
                'IS_Item Condition': self.is_item_condition,
                'eBay Payment Preset Name': self.ebay_payment_preset_name,
                'eBay Preset Wrapper Name': self.ebay_preset_wrapper_name,
                'eBay Description Wrapper Name': self.ebay_description_wrapper_name,
                'ebay Shipping Preset Name': self.ebay_shipping_preset_name,
                'Picture': self.picture_url,
                'Pictures Manual Picture URL': self.picture_url,
                'eBay Description': self.ebay_description}

        return part

    def set_all(self):
        self.set_sku()
        self.set_title()
        self.set_where_used_html()
