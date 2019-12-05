from . import db

class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    image = db.Column(db.String(10))
    minPrice = db.Column(db.Integer)
    maxPrice = db.Column(db.Integer)

class MatchingProduct(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    matching_id = db.Column(db.Integer)
    imageUrl = db.Column(db.String(100)) 
    productUrl = db.Column(db.String(100))

    
