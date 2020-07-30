import csv
import json
import urllib.request
import sys

base_url = sys.argv[1]
url = base_url + '/products.json'

def get_page(page):
    data = urllib.request.urlopen(url + '?page={}'.format(page)).read()
    products = json.loads(data)['products']
    return products
  
with open('andreas.csv', 'w', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Description',  'Price', 'SKU', 'Image'])
    page = 1
    products = get_page(page)
    while products:
        for product in products:
            name = product['title']
            html = product['body_html']
            images =[]
            for image in product['images']:
                src = image['src']
                imageURL = src.split("?")[0]
                images.append(imageURL)
            for variant in product['variants']:
                price = variant['price']
                if variant['sku'] is None:
                    continue
                sku = variant['sku']
                for image in images:

                    if image == images[0]:
                        unique_row = [name, html, price, sku, images[0]]
                        unique_row = [c.encode("utf-8").decode("utf-8") for c in unique_row]
                        writer.writerow(unique_row)

                    row = [ '', '', '', '', image]
                    row = [c.encode("utf-8").decode("utf-8") for c in row]
                    writer.writerow(row)
        page += 1
        print(page)
        print(len(products))
        products = get_page(page)
