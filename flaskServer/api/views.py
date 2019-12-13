from flask import Blueprint, jsonify, request
from . import db 
from .models import Product,MatchingProduct
from .fetcher import fetchClostestImages
import time 

main = Blueprint('main', __name__)

@main.route('/add_product', methods=['POST'])
def add_product():
    print("Added product")
    product_data = request.get_json()
    matching_id=product_data['id']
    base64_image=product_data['image'].rstrip()
    new_product = Product(id=matching_id,image=base64_image, minPrice=product_data['minPrice'], maxPrice=product_data['maxPrice'])
    db.session.add(new_product)
    db.session.commit()
    fetched_list = fetchClostestImages(product_data,matching_id)
    add_matching_products(fetched_list)
    return 'Done', 201

@main.route('/products')
def products():
    # print("showing products")
    product_list = Product.query.all()
    products = []
    for product in product_list:
        products.append({'id':product.id,'image' : product.image, 'minPrice' : product.minPrice, 'maxPrice' : product.maxPrice})
    return jsonify( products)

@main.route('/get_matches')
def get_matching_products():
    matching_product_list = MatchingProduct.query.all()
    products = []
    for product in matching_product_list:
        products.append({
            'id':product.id, 
            'rank' : product.rank,
            'name':product.name,
            'price':product.price ,
            'matching_id' : product.matching_id,
            'imageUrl' : product.imageUrl, 
            'productUrl' : product.productUrl})
    return jsonify(products)

def add_matching_products(fetched_list):
   for matching_product in fetched_list:
       db.session.add(matching_product)
       db.session.commit()
    
def get_time_current_millis():
    return round(time.time()*10000)