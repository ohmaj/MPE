

class Parts_Tree_Model:

    def __init__(self):
        self.item_id = ''
        self.part_id = ''
        self.part_description = ''
        self.compatable_machines = ''
        self.part_thumbnail_src = ''
        self.header_row = ['Item ID','Product ID', 'Description', 'Where Used', 'Thumbnail URl']
        self.as_list = ''

    def get_as_list(self):
        self.as_list = [self.item_id, self.part_id, self.part_description, self.compatable_machines, self.part_thumbnail_src]