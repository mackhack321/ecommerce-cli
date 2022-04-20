from dbOpenConn import openDBConnection

class Item:
    def __init__(self, id, title, genre, director, rating, year, price, quantity):
        self.id = id
        self.title = title
        self.genre = genre
        self.director = director
        self.rating = rating
        self.year = year
        self.price = price
        self.quantity = quantity
    
    def canRemoveStock(self, qty):
        return self.quantity >= qty