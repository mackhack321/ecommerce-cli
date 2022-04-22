from dbOpenConn import openDBConnection

class Inventory:
    def __init__(self):
        self.items = []
        self.update()
    
    def removeItemStock(self, id, qty):
        ...
    
    def update(self):
        ...