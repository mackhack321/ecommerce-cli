#Moviesfile
from dbOpenConn import openDBConnection

class Movie:
    def __init__(self, id, title, genre, director, rating, year, price, quantity):
        self.movieID = id
        self.title = title
        self.genre = genre
        self.director = director
        self.rating = rating
        self.year = year
        self.price = price
        self.quantity = quantity

    def canRemoveStock(self, qty): 
        return self.quantity >= qty
