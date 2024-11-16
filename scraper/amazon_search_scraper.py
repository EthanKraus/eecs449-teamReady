import requests
import pandas as pd
from bs4 import BeautifulSoup
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from pymongo import UpdateOne
import argparse
import json


# Options:
# #######################################
# category = "fashion"
# keyword = "pants"
# max_links_num = 1000
# #######################################


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8'
}

# db_url = "mongodb+srv://tzb:123qweasdzxc@cluster0.ly0rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(db_url, server_api=ServerApi('1'))
# db = client["449project"]
# col = db["search_page_data"]
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
# col.create_index("ASIN", unique=True)


def get_soup(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")
    return soup


def search_scraping(search_url, category, keyword, max_links_num, current_link_num=0):

    print("---------------------------------------------------------------")
    print(f"Scraping page URL: {search_url}")
    print(f"Link count: {current_link_num}")

    soup = get_soup(search_url)
    product_elements = soup.select('div[data-component-type="s-search-result"]')
    page_data = []

    for product_element in product_elements:
        if current_link_num >= max_links_num:
            print(f"Reached limit of {max_links_num} links.")
            break

        ASIN_element = product_element.get('data-asin')
        ASIN = ASIN_element if ASIN_element else None

        title_element = product_element.select_one('div[data-cy="title-recipe"]>h2>a>span')
        title = title_element.text.strip() if title_element else None

        price_element = product_element.select_one("span.a-offscreen")
        price_text = price_element.text[1:] if price_element else None 
        price = float(price_text.replace(',', '')) if price_text else None

        rating_element = product_element.select_one('i[data-cy="reviews-ratings-slot"]')
        rating_text = rating_element.text if rating_element else None
        rating = float(rating_text.replace(" out of 5 stars", "")) if rating_text else None

        image_element = product_element.select_one('.s-image')
        image = image_element.attrs.get("src") if image_element else None

        # product_url_element = product_element.select_one('div[data-cy="title-recipe"]>h2>a')
        product_url = "https://www.amazon.com/dp/" + ASIN

        product_info = {
            "ASIN": ASIN,
            "title": title,
            "price": price,
            "rating": rating,
            "image": image,
            "search_url": search_url,
            "product_url": product_url,
            "category": category,
            "keyword": keyword
        }
        # print(product_info)
        page_data.append(product_info)
        current_link_num += 1

    # # Insert to MongoDB.
    # if page_data:
    #     operations = []
    #     for product_info in page_data:
    #         operation = UpdateOne({"ASIN": product_info["ASIN"]}, {"$set": product_info}, upsert=True)
    #         operations.append(operation)

    #     if operations:
    #         result = col.bulk_write(operations)
    #         print(f"Performed {len(operations)} update operations.")
    #         print(f"Inserted {result.upserted_count} new documents and updated {result.modified_count} existing documents.")

    # If we haven't reached the max links and there is a next page, scrape the next page
    if current_link_num < max_links_num:
        next_page_element = soup.select_one('a.s-pagination-next')
        if next_page_element:
            next_page_url = "https://www.amazon.com" + next_page_element.attrs.get('href')
            page_data += search_scraping(next_page_url, category, keyword, max_links_num, current_link_num)
        else:
            print(f"Reached the final page. Scraping has ended. Scraped {current_link_num} links in total.")

    return page_data


def main():
    parser = argparse.ArgumentParser(description="Script to search for fashion items.")
    parser.add_argument("-c", "--category", type=str, required=True, help="Category of items to search for (e.g., 'fashion').")
    parser.add_argument("-k", "--keyword", type=str, required=True, help="Keyword to search for within the category (e.g., 'pants').")
    parser.add_argument("-m", "--max_links_num", type=int, default=1000, help="Maximum number of links to retrieve.")
    args = parser.parse_args()

    category = args.category
    keyword = args.keyword
    max_links_num = args.max_links_num
    print(f"Category: {category}, Keyword: {keyword}, Max number of links: {max_links_num}")

    search_url = f"https://www.amazon.com/s?k={keyword}&i={category}"
    data = search_scraping(search_url, category, keyword, max_links_num)
    df = pd.DataFrame(data)
    df.to_csv("amazon_search_scraper_results.csv")

    json_data = json.dumps(data, indent=4)
    print(json_data)


if __name__ == '__main__':
    main()
