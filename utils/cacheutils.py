import json
import os
from typing import List, Dict

def readCachedData(file_path: str) -> List[Dict]:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def overrideCachedData(file_path: str, data: List[Dict]):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def updateCache(file_path: str, products: List[Dict]):
    cachedData = readCachedData(file_path)
    product_dict = {p['title']: p for p in cachedData}

    for product in products:
        title = product['title']
        if title in product_dict:
            if product_dict[title]['price'] != product['price']:
                product_dict[title] = product
        else:
            product_dict[title] = product
        
    overrideCachedData(file_path, list(product_dict.values()))
