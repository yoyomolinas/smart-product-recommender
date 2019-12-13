from .models import MatchingProduct
# from os import path
# import sys

# featex_module_path = path.abspath(path.join(__file__, '../../../'))
# print("Featex module path", featex_module_path)

# sys.path.append(featex_module_path)
from .imageFeatureExtractorV2.api import API

FEATEX_API = API(model_name = "pretrained-mobilenet-v2-1-100", debug = False)

def fetchClostestImages(imageData, matchingid, k = 16):
    """
    This imageData object will be in the form of :
    id, imageBase64String, minPrice, maxPrice  
    """
    # rstrip image to remove \n in base 64 string
    image_base64 = imageData['image'].rstrip()
    minimum_price = imageData['minPrice']
    maximum_price = imageData['maxPrice']
    #TODO: do whatever you want to do here with the image
    returned_products = []
    print("Fetching closest images for %i"%matchingid)
    query_df = FEATEX_API.get_closest_neighbors(image_base64, k=k, min_price=minimum_price, max_price=maximum_price)

    #Encode query results in MatchingProduct format 
    for i, (_, row) in enumerate(query_df.iterrows()):
        new_product = MatchingProduct(
            matching_id=matchingid,
            rank = i,
            name=row['productname'],
            price=row['productprice'], 
            imageUrl=row['productimageurl'],
            productUrl=row['producturl'])
        returned_products.append(new_product)
    
    print("Number of returned products:",len(returned_products))
    return returned_products