from .models import MatchingProduct
def fetchClostestImages(imageData,matchingid):
    """
    This imageData object will be in the form of :
    id, imageBase64String, minPrice, maxPrice  
    """
    returned_products = []
    
    #TODO We must fill the above array with 10 closest images. You have three inputs from imageData object:
    # imageBase64String
    # minPrice
    # maxPrice
    print("Image data is the following:")
    print(matchingid)

    for i in range(10):
        
        print("I am getting Yoel's images (This is my bro Yoel's part) ")    
        new_product = MatchingProduct(matching_id=matchingid,name="dummy_name",price=50, imageUrl='www.dummy.com/'+str(i), productUrl='www.dummy.com/'+str(i))
        returned_products.append(new_product)
    
    return returned_products 

    