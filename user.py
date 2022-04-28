from dbOpenConn import openDBConnection
from datetime import date

class User:
    def __init__(self):
        self.userID = -1
        self.isLoggedIn = False
        self.firstname = ""
        self.lastname = ""

    def setUserID(self, id):
        self.userID = id
    
    def setShippingInformation(self, address, pobox, city, state, zip):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        # check if the user already has shipping information
        if not self.getShippingInformation(): # need to make new entry in table
            query = "INSERT INTO shipping_info (userID, address, pobox, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (str(self.userID), address, pobox, city, state, zip)

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False
        
        else: # just update the existing info
            query = f"UPDATE shipping_info SET address=%s, pobox=%s, city=%s, state=%s, zip=%s WHERE userID=%s"
            data = (address, pobox, city, state, zip, str(self.userID))

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False

        cursor.close()
        db.close()

        return success

    def setPaymentInformation(self, cardNumber, expirationDate, zip, securityCode):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        # check if the user already has payment information
        if not self.getPaymentInformation(): # need to make new entry in table
            query = "INSERT INTO payment_info (userID, cardNumber, expirationDate, zip, securityCode) VALUES (%s, %s, %s, %s, %s)"
            data = (str(self.userID), cardNumber, expirationDate, zip, securityCode)

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False
        
        else: # just update the existing info
            query = "UPDATE payment_info SET cardNumber=%s, expirationDate=%s, zip=%s, securityCode=%s WHERE userID=%s"
            data = (cardNumber, expirationDate, zip, securityCode, str(self.userID))

            try:
                cursor.execute(query, data)
                db.commit()
            except:
                success = False

        cursor.close()
        db.close()

        return success

    def getShippingInformation(self):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = f"SELECT * FROM shipping_info WHERE userID=%s"
        data = (str(self.userID), )

        cursor.execute(query, data)
        
        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result

    def getPaymentInformation(self):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = f"SELECT * FROM payment_info WHERE userID=%s"
        data = (str(self.userID), )

        cursor.execute(query, data)
        
        result = cursor.fetchall()

        cursor.close()
        db.close()

        return result
    
    def getOrderHistory(self):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM order_history WHERE userID=%s"
        data = (str(self.userID), )

        cursor.execute(query, data)
        result = cursor.fetchall()

        hist = []

        for order in result:
            movieQuery = "SELECT * FROM movies WHERE movieID=%s"
            movieData = (order['movieID'], )

            cursor.execute(movieQuery, movieData)
            movie = cursor.fetchall()

            title = movie[0]['title']
            quantity = order['quantity']
            price = movie[0]['price']
            date=order['date']
            hist.append({"title" : title, "quantity" : quantity, "price" : price, "date" : date})

        cursor.close()
        db.close()

        return hist
    
    def addOrderToHistory(self, movieID, quantity):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "INSERT INTO order_history (userID, movieID, quantity, date) VALUES (%s, %s, %s, %s)"
        data = (self.userID, movieID, quantity, date.today().strftime("%m/%d/%Y"))

        try:
            cursor.execute(query, data)
            db.commit()
        except:
            success = False
        
        cursor.close()
        db.close()

        return success
    
    def login(self, username, password):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = f"SELECT * FROM users WHERE username=\"{username}\" AND password=\"{password}\""
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 1:
            user = result[0]
            self.setUserID(user["userID"])
            self.isLoggedIn = True
            self.firstname = user["firstname"]
            self.lastname = user["lastname"]

        cursor.close()
        db.close()

        return self.isLoggedIn
    
    def logout(self):
        self.isLoggedIn = False

    def delete(self):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)
        success = True

        tablesToDeleteFrom = ["shipping_info", "payment_info", "order_history", "cart", "users"]

        for table in tablesToDeleteFrom:
            query = f"DELETE FROM {table} WHERE userID=\"{self.userID}\""

            try:
                cursor.execute(query)
                db.commit()
                self.logout()
            except:
                success = False
        
        cursor.close()
        db.close()

        return success 

    def createAccount(self, username, password, firstname, lastname):
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)
        success = True

        query = f"INSERT INTO users (username, password, firstname, lastname) VALUES (%s, %s, %s, %s)"
        data = (username, password, firstname, lastname)

        try:
            cursor.execute(query, data)
            db.commit()

        except:
            success = False

        return success