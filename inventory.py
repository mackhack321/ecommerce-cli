from dbOpenConn import openDBConnection
from movie import Movie

class Inventory:
    def __init__(self):
        self.items = []
        self.update()
    
    def removeItemStock(self, id, qty):
        success = True

        for item in self.items:
            if item.id == id and not item.canRemoveStock(qty):
                success = False
                return success

        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "UPDATE movies SET quantity=quantity-%s WHERE movieID=%s"
        data = (qty, id)

        try:
            cursor.execute(query, data)
            db.commit()
        except:
            success = False
        
        cursor.close()
        db.close()

        self.update()

        return success

    
    def update(self):
        ...