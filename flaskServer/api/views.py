from flask import Blueprint, jsonify, request
from . import db 
from .models import Product

main = Blueprint('main', __name__)

@main.route('/add_product', methods=['POST'])
def add_product():
    product_data = request.get_json()
    new_product = Product(image=product_data['image'], minPrice=product_data['minPrice'], maxPrice=product_data['maxPrice'])
    db.session.add(new_product)
    db.session.commit()
    return 'Done', 201

@main.route('/products')
def products():
    product_list = Product.query.all()
    products = []
    for product in product_list:
        products.append({'id':product.id,'image' : product.image, 'minPrice' : product.minPrice, 'maxPrice' : product.maxPrice})
    return jsonify({'uploaded_products' : products})