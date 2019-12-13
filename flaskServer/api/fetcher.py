from .models import MatchingProduct
# from os import path
# import sys

# featex_module_path = path.abspath(path.join(__file__, '../../../'))
# print("Featex module path", featex_module_path)

# sys.path.append(featex_module_path)
# from imageFeatureExtractorV2.api import API

# FEATEX_API = API()

def fetchClostestImages(imageData, matchingid):
    """
    This imageData object will be in the form of :
    id, imageBase64String, minPrice, maxPrice  
    """
    yoels_image = imageData['image'].rstrip()
    minimum_price = imageData['minPrice']
    maximum_price = imageData['maxPrice']
    #TODO: do whatever you want to do here with the image
    returned_products = []
    
    #TODO We must fill the above array with 10 closest images. You have three inputs from imageData object:
    # imageBase64Strings
    # minPrice
    # maxPrice
    print("Image data is the following:")
    print(matchingid)
    print("I am getting Yoel's images (This is my bro Yoel's part) ")    

    for i in range(10):
    
        new_product = MatchingProduct(matching_id=matchingid,name="dummy_name",price=50, imageUrl='www.dummy.com/'+str(i), productUrl='www.dummy.com/'+str(i))
        returned_products.append(new_product)
    
    return returned_products 

    