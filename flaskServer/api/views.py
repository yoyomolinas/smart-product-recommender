from flask import Blueprint, jsonify, request
from . import db 
from .models import Product,MatchingProduct
from .fetcher import fetchClostestImages

main = Blueprint('main', __name__)

@main.route('/add_product', methods=['POST'])
def add_product():
    product_data = request.get_json()
    new_product = Product(image=product_data['image'], minPrice=product_data['minPrice'], maxPrice=product_data['maxPrice'])
    db.session.add(new_product)
    db.session.commit()
    fetched_list = fetchClostestImages(product_data)
    add_matching_products(fetched_list)
    return 'Done', 201

@main.route('/products')
def products():
    product_list = Product.query.all()
    products = []
    for product in product_list:
        products.append({'id':product.id,'image' : product.image, 'minPrice' : product.minPrice, 'maxPrice' : product.maxPrice})
    return jsonify({'uploaded_products' : products})

@main.route('/get_matches/<int:product_id>')
def get_matching_products(product_id):
    products = []
    for product in product_list:
        products.append({'id':product.id,'image' : product.image, 'minPrice' : product.minPrice, 'maxPrice' : product.maxPrice})
    return jsonify({'uploaded_products' : products})

def add_matching_products(fetched_list):
   for x in fetched_list:
       db.session.add(matching_products)
       db.session.commit()
    
   