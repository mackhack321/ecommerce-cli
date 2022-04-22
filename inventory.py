from dbOpenConn import openDBConnection

class Inventory:
    def __init__(self):
        self.items = []
        self.update()
    
    def removeItemStock(self, id, qty):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)
        success = True

        query = f"UPDATE movies SET quantity=%s WHERE movieID=%s"
        data = (qty, id)

        try:
            cursor.execute(query, data)
            db.commit()
        except:
            success = False

        cursor.close()
        db.close()

        return success

    
    def update(self):
        ...