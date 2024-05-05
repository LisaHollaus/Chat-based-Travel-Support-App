from .traveller import User

#### inherits base too?
## needed?

class Provider(User):
    def __init__(self, name, address, id):
        super().__init__(name, address, id)
        # self.attractions = [] inherited from Traveller