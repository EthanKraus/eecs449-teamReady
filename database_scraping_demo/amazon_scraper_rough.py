import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.parse
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateOne


# Options:
#######################################
# url = "https://www.amazon.com/s?k=dress&i=fashion&rh=n%3A7141123011&dc&ds=v1%3AeacFGCPFn79ZQtM5O5O%2BSSkXTg%2FPzV6G%2FirKb50pRWY&crid=1WVQDRLF5ACTM&qid=1727930661&rnid=85457740011&sprefix=dress%2Caps%2C105&ref=sr_nr_p_123_1"
keyword = "skirt"
category = "i=fashion"
max_links_num = 1000
#######################################


visited_urls_num = set()
# category = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('k', [''])[0]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8'
}

uri = "mongodb+srv://tzb:123qweasdzxc@cluster0.ly0rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["449project"]
col = db["products_rough"]
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
col.create_index("ASIN", unique=True)


def generate_amazon_search_url(keyword, category):
    base_url = "https://www.amazon.com/s"
    return f"{base_url}?k={keyword}&{category}"


def get_soup(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")
    return soup


def search_scraping(url, current_link=0):
    global visited_urls_num

    print("---------------------------------------------------------------")
    print(f"Scraping page URL: {url}")
    print(f"Link count: {current_link}")

    soup = get_soup(url)
    product_elements = soup.select('div[data-component-type="s-search-result"]')
    page_data = []

    for product_element in product_elements:
        if current_link >= max_links_num:
            print(f"Reached limit of {max_links_num} links.")
            break

        ASIN_element = product_element.get('data-asin')
        ASIN = ASIN_element if ASIN_element else None

        title_element = product_element.select_one('div[data-cy="title-recipe"]>h2>a>span')
        title = title_element.text.strip() if title_element else None

        price_element = product_element.select_one("span.a-offscreen")
        price_text = price_element.text[1:] if price_element else None  # Removing '$'
        price = float(price_text.replace(',', '')) if price_text else None

        rating_element = product_element.select_one('i[data-cy="reviews-ratings-slot"]')
        rating_text = rating_element.text if rating_element else None
        rating = float(rating_text.replace(" out of 5 stars", "")) if rating_text else None

        image_element = product_element.select_one('.s-image')
        image = image_element.attrs.get("src") if image_element else None

        product_info = {
            "ASIN": ASIN,
            "title": title,
            "price": price,
            "rating": rating,
            "image": image,
            "url": url,
            "category": category
        }
        # print(product_info)
        page_data.append(product_info)
        current_link += 1

    if page_data:
        operations = []
        for product_info in page_data:
            operation = UpdateOne({"ASIN": product_info["ASIN"]}, {"$set": product_info}, upsert=True)
            operations.append(operation)

        if operations:
            result = col.bulk_write(operations)
            print(f"Performed {len(operations)} update operations.")
            print(f"Inserted {result.upserted_count} new documents and updated {result.modified_count} existing documents.")

    if current_link < max_links_num:
        next_page_el = soup.select_one('a.s-pagination-next')
        if next_page_el:
            next_page_url = next_page_el.attrs.get('href')
            next_page_url = urllib.parse.urljoin(url, next_page_url)
            page_data += search_scraping(next_page_url, current_link)
        else:
            print(f"Reached the final page. Scraping has ended. Scraped {visited_urls_num} links in total.")

    return page_data


def main():
    url = generate_amazon_search_url(keyword, category)
    data = []
    data = search_scraping(url)
    df = pd.DataFrame(data)
    df.to_csv("input_data_rough.csv")


if __name__ == '__main__':
    main()
