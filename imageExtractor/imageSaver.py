import urllib.request
import csv
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path+'/productImageFeed.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        image_url = row['productimageurl']
        line_count+=1
        #For limiting the test
        if(line_count) == 20:
            break
        image_path = dir_path+'/photo%d.jpg ' % line_count
        print(image_path)
        # f = open(image_path,'wb')
        # f.write(urllib.request.urlopen(image_url).read())
        # f.close()
