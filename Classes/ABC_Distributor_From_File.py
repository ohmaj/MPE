from abc import abstractmethod
from Classes import Distrib_New


class ABCDistributorFromFile(Distrib_New.Distributor):

    def __init__(self, mfr):
        super().__init__(mfr)

    def get_distributor_inventory_dictionary(self):
        distributor_inventory = self.parse_file_to_dictionary()
        return distributor_inventory

    @abstractmethod
    def parse_file_to_dictionary(self):
        pass
