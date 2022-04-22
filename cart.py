from operator import truediv
from dbOpenConn import openDBConnection
from datetime import date


class Cart:
    def __init__(self):
        pass

    def addItem(self, userID, movieID, qty):
        success = True
        db = openDBConnection()
        cursor = db.cursor(dictionary=True)

        query = "INSERT INTO cart(userID, movieID, quantity) VALUES (%s, %s, %s,)"
        data = (self.userID, movieID, qty, date.today().strftime("%m/%d/%Y"))
