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
    
    def removeItem(self, userID, movieID):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "DELETE FROM cart WEHERE userID = %s AND movieID = %s"
        data = (userID, movieID)
        try:
            cursor.execute(query, data)
            db.commit()
        except:
            success = False 
        if cursor.rowcount == 0:
            success = False 
        cursor.close()
        db.close()
        return success
    
    def checkout(self, user, inventory):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM cart WHERE userID = %s"
        data = (user.userID, )
        cursor.execute(query, data)
        Items = cursor.fetchall()
        for item in Items: 
            if not inventory.removeItemStock(item['movieID'], item['quantity']):
                success = False 
                return success
            if not user.addOrderToHistory(item['movieID'], item['quantity']):
                success = False 
                return success
            query = "DELETE FROM cart WHERE userID = %s"
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
        cursor = db.curosr(dictionary=True)
        query = "SELECT * FROM cart WHERE userID = %s"
        data = (userID, )
        cursor.execute(query, data)
        data = cursor.fetchall()
        dataList = []
        for entry in data: 
            query = "SELECT * FROM movies where movieID = %s"
            data = (entry['movieID'], )
            cursor.execute(query, data)
            movie = cursor.fetchall()
            dataList.append({"movieID: ": entry['movieID'], "title: ": movie[0]['title'], "quantity: ": entry['quantity']})
        cursor.close()
        db.close()
        return dataList
    
    def getCost(self, userID):
        db = openDBConnection()
        cursor = db.cursor(dictoionary=True)
        query = "SELECT * FROM cart WHERE userID = %s"
        data = (userID, )
        cursor.execute(query, data)
        data = cursor.fetchall()
        Total = 0.0
        
        for entry in data: 
            query = "SELECT * FROM movies WHERE movieID = %s"
            data = (entry['movieID'], )
            cursor.execute(query, data)

            movie = cursor.fetchall()
            Total += float(movie[0]['price']) * int(entry['quantity'])
        cursor.close()
        db.close()
        return Total

