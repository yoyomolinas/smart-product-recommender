from . import db

class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    image = db.Column(db.String(10))
    minPrice = db.Column(db.Integer)
    maxPrice = db.Column(db.Integer)
