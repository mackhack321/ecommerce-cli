from dbOpenConn import openDBConnection
from datetime import date


class Cart:
    def __init__(self):
        pass
    
    def addItem(self, userID, movieID, qty):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "INSERT INTO cart(userID, movieID, quantity) VALUES(%s,%s,%s)"
        data = (userID, movieID, qty)

        try:
            cursor.execute(query, data)
            db.commit()
        except:
            success = False

        cursor.close()
        db.close()
        
        return success

    def removeItem(self, userID, movieID):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "DELETE FROM cart WHERE userID=%s AND movieID=%s"
        data = (userID, movieID)

        try:
            cursor.execute(query, data)
            db.commit()
        except:
            success = False

        cursor.close()
        db.close()
        
        return success
    
    def checkout(self, user, inventory):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM cart WHERE userID=%s"
        data = (user.userID, )

        cursor.execute(query, data)
        cartItems = cursor.fetchall()

        for item in cartItems:
            # add stuff to user's order history
            query = "INSERT INTO order_history (userID, movieID, quantity, date) VALUES (%s, %s, %s, %s)"
            data = (user.userID, item['movieID'], item['quantity'], date.today().strftime("%m/%d/%Y"))

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False

            # remove stuff from inventory
            inventory.removeItemStock(item['movieID'], item['quantity'])

            # remove stuff from cart
            query = "DELETE FROM cart WHERE userID=%s"
            data = (user.userID, )

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False

        cursor.close()
        db.close()

        return success

    def getCart(self, userID):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM cart WHERE userID=%s"
        data = (userID, )

        cursor.execute(query, data)

        data = cursor.fetchall()

        cursor.close()
        db.close()

        return data
