from flask import Blueprint, jsonify, request, render-templete
from . import db 
from .models import Product,MatchingProduct
from .fetcher import fetchClostestImages
import time 

main = Blueprint('main', __name__)

@main.route('/add_product', methods=['POST'])
def add_product():
    print("added product")
    product_data = request.get_json()
    
    #Normally this currenttime field will come from the mobile application
    currentTime = get_time_current_millis()
    new_product = Product(id=currentTime,image=product_data['image'], minPrice=product_data['minPrice'], maxPrice=product_data['maxPrice'])
    db.session.add(new_product)
    db.session.commit()
    fetched_list = fetchClostestImages(product_data,currentTime)
    print(fetched_list)
    add_matching_products(fetched_list)
    return 'Done', 201

@main.route('/products')
def products():
    print("showing products")
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
        products.append({'id':product.id,'matching_id' : product.matching_id, 'imageUrl' : product.imageUrl, 'productUrl' : product.productUrl})
    return jsonify(products)

@main.route('/admin_benchmark')
def show_admin_page():
    render-templete('/adminPage/admin.html');

def add_matching_products(fetched_list):
   for matching_product in fetched_list:
       db.session.add(matching_product)
       db.session.commit()

# @main.route('/add_matching_product', methods=['POST'])
# def add_matching_product():
#     matching_product_data = request.get_json()
#     new_matching_product = MatchingProduct(matching_id=matching_product_data['matching_id'],imageUrl=matching_product_data['imageUrl'], productUrl=matching_product_data['productUrl'])
#     db.session.add(new_matching_product)
#     db.session.commit()
#     # fetched_list = fetchClostestImages(product_data)
#     # add_matching_products(fetched_list)
#     return 'Done', 201  
    
def get_time_current_millis():
    return round(time.time()*10000)