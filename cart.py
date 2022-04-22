from dbOpenConn import openDBConnection


class Cart:
    def __init__(self):
        pass

    def addItem(self, userID, movieID, qty):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "INSERT INTO cart(userID, movieID, quantity) VALUES (%s, %s, %s)"
        data = (userID, movieID, qty)
        try:
            cursor.execute(query, data)
            db.commit()
        except:
            success = False
        cursor.close()
        db.close()
        return success
