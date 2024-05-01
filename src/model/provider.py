from .traveller import Traveller

class Provider(Traveller):
    def __init__(self, name, address, traveller_id):
        super().__init__(name, address, traveller_id)
        # self.attractions = [] inherited from Traveller