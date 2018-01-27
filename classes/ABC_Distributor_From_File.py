from abc import abstractmethod
from classes import ABC_Distributor


class ABCDistributorFromFile(ABC_Distributor.Distributor):

    def __init__(self, mfr):
        super().__init__(mfr)

    def get_distributor_inventory_dictionary(self):
        distributor_inventory = self.parse_file_to_dictionary()
        return distributor_inventory

    @abstractmethod
    def parse_file_to_dictionary(self):
        pass
