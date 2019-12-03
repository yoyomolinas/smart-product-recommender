from .models import MatchingProduct
def fetchClostestImages(imageData):
    returned_products = []
    for i in range(10):
        print("I am getting Yoel's images (This is my bro Yoel's part) ")    
        new_product = MatchingProduct(matching_id=imageData['id'], imageUrl='www.dummy.com/'+i, productUrl='www.dummy.com/'+i])
        returned_products.append(new_product)
    return returned_products 

    