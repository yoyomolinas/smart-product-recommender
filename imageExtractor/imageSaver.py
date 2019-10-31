import urllib.request
import csv
import pandas as pd
import keras
import os
#dir_path = os.path.dirname(os.path.realpath(__file__))
#with open(dir_path+'/productImageFeed.csv', mode='r') as csv_file:
#    csv_reader = csv.DictReader(csv_file)
#    line_count = 0
#    for row in csv_reader:
#        image_url = row['productimageurl']
#        line_count+=1
#        #For limiting the test
#        if(line_count) == 20:
#            break
#        image_path = dir_path+'/photo%d.jpg ' % line_count
#        print(image_path)
        #Uncomment below lines to downlaod the images
        # f = open(image_path,'wb')
        # f.write(urllib.request.urlopen(image_url).read())
        # f.close()

def read_data():
    with open("productImageFeed.csv", encoding='utf-8') as csvfile:
        product_urls = []
        product_category = []
        readCSV = csv.DictReader(csvfile)
        for row in readCSV:
            product_urls.append(row['productimageurl'])
            product_category.append(row['productcategory'])
        dataset = {'productimageurl': product_urls, 'productcategory': product_category}
        df = pd.DataFrame(data=dataset)
        return df
