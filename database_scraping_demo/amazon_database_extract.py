import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Options:
#######################################
collection_name = "products_rough"
query_filter = {
    'category': 'pants',
    'price': {'$gt': 20},
    'rating': {'$gt': 4.5}
    }
#######################################


extract_options = {
    # '_id': 1,
    'ASIN': 1,
    'category': 1,
    'image': 1,
    'price': 1,
    'rating': 1,
    'title': 1,
    'url': 1
}

uri = "mongodb+srv://tzb:123qweasdzxc@cluster0.ly0rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["449project"]
col = db[collection_name]

documents = col.find(query_filter, extract_options)

extracted_data = []
for doc in documents:
    extracted_element = {
        # "_id": str(doc.get('_id')),
        "ASIN": doc.get('ASIN'),
        "category": doc.get('category'),
        "image": doc.get('image'),
        "price": doc.get('price'),
        "rating": doc.get('rating'),
        "title": doc.get('title'),
        "url": doc.get('url')
    }
    extracted_data.append(extracted_element)

df = pd.DataFrame(extracted_data)
df.to_csv("extracted_data.csv", index=False)

print(f"Number of data extracted: {len(extracted_data)}")