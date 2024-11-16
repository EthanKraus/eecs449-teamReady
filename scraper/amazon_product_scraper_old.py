import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateOne


# Options:
#######################################
category = "fashion"
keyword = "pants"
max_links = 100
#######################################


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8'
}

search_url = "https://www.amazon.com/s?k=dress&crid=3Q5682YRVSU5N&sprefix=%2Caps%2C89&ref=nb_sb_ss_recent_1_0_recent"
visited_urls = set()

uri = "mongodb+srv://tzb:123qweasdzxc@cluster0.ly0rn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["449project"]
col = db["product_page_data"] 
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def generate_amazon_search_url(category, keyword):
    base_url = "https://www.amazon.com/s"
    return f"{base_url}?k={keyword}&i={category}"


def get_soup(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    soup = BeautifulSoup(response.text, "lxml")
    return soup


### Can't scrape review page, will be stuck to captcha, so this function doesn't work right now. ###
# def get_reviews(reviews_url):
#     print(f"Scraping reviews from {reviews_url}")
#     soup = get_soup(reviews_url)
#     # with open("reviews_page", "w", encoding="utf-8") as f:
#     #     f.write(soup.prettify())

#     review_elements = soup.select("div.review")
#     # print(review_elements)

#     scraped_reviews = []

#     for review in review_elements:
#         r_author_element = review.select_one("span.a-profile-name")
#         r_author = r_author_element.text if r_author_element else None

#         r_rating_element = review.select_one("i.review-rating")
#         r_rating = r_rating_element.text.replace("out of 5 stars", "") if r_rating_element else None

#         r_title_element = review.select_one("a.review-title")
#         r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
#         r_title = r_title_span_element.text if r_title_span_element else None

#         r_content_element = review.select_one("span.review-text")
#         r_content = r_content_element.text if r_content_element else None

#         r_date_element = review.select_one("span.review-date")
#         r_date = r_date_element.text if r_date_element else None

#         r_verified_element = review.select_one("span.a-size-mini")
#         r_verified = r_verified_element.text if r_verified_element else None

#         r_image_element = review.select_one("img.review-image-tile")
#         r_image = r_image_element.attrs["src"] if r_image_element else None

#         r = {
#             "author": r_author,
#             "rating": r_rating,
#             "title": r_title,
#             "content": r_content,
#             "date": r_date,
#             "verified": r_verified,
#             "image_url": r_image
#         }

#         scraped_reviews.append(r)

#     return scraped_reviews


# Get reviews in the product page. Temperary substitute.
def get_product_page_reviews(soup):
    review_elements = soup.select("div.review")
    # print(review_elements)

    reviews = []

    for review in review_elements:
        r_author_element = review.select_one("span.a-profile-name")
        r_author = r_author_element.text if r_author_element else None

        r_rating_element = review.select_one("i.review-rating")
        r_rating = r_rating_element.text.replace("out of 5 stars", "") if r_rating_element else None

        r_title_element = review.select_one("a.review-title")
        r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None

        r_content_element = review.select_one("span.review-text")
        r_content = r_content_element.text if r_content_element else None

        r_date_element = review.select_one("span.review-date")
        r_date = r_date_element.text if r_date_element else None

        r_verified_element = review.select_one("span.a-size-mini")
        r_verified = r_verified_element.text if r_verified_element else None

        r_image_element = review.select_one("img.review-image-tile")
        r_image = r_image_element.attrs["src"] if r_image_element else None

        r = {
            "author": r_author,
            "rating": r_rating,
            "title": r_title,
            "content": r_content,
            "date": r_date,
            "verified": r_verified,
            "image_url": r_image
        }

        reviews.append(r)

    return reviews


def get_product_info(product_url, search_url):
    print(f"Scraping product from {product_url[:100]}", flush=True)
    soup = get_soup(product_url)
    # with open("product_page", "w", encoding="utf-8") as f:
    #     f.write(soup.prettify())

    ASIN_element = soup.find('span', string=lambda text: text and "ASIN" in text).find_next_sibling('span')
    ASIN = ASIN_element.text.strip() if ASIN_element else None

    title_element = soup.select_one("#productTitle")
    title = title_element.text.strip() if title_element else None

    price_elements = soup.find_all('span', class_='a-price a-text-price a-size-medium apexPriceToPay')
    if price_elements:
        price = [float(price.find('span', class_='a-offscreen').text.strip().replace('$', '')) for price in price_elements]
    else:
        whole = soup.find('span', class_='a-price-whole').get_text()
        fraction = soup.find('span', class_='a-price-fraction').get_text()
        price = [whole + fraction]

    rating_element = soup.select_one("#acrPopover")
    rating_text = rating_element.attrs.get("title") if rating_element else None
    rating = rating_text.replace("out of 5 stars", "") if rating_text else None

    image_element = soup.select_one("#landingImage")
    image = image_element.attrs.get("src") if image_element else None

    description_element = soup.select_one("#productDescription")
    description = description_element.text.strip() if description_element else None

    reviews_url_element = soup.select_one("a[data-hook='see-all-reviews-link-foot']")
    reviews_url = urljoin("https://www.amazon.com", reviews_url_element.attrs.get("href")) if reviews_url_element else None

    # reviews = get_reviews(reviews_url) if reviews_url else []
    reviews = get_product_page_reviews(soup) if reviews_url else []

    return {
        "ASIN": ASIN,
        "title": title,
        "price": price,
        "rating": rating,
        "image": image,
        "description": description,
        "reviews": reviews,
        "search_url": search_url,
        "product_url": product_url,
        "category": category,
        "keyword": keyword
    }


def parse_listing(search_url, max_links=10, max_pages=1, current_link=0, current_page=0):
    global visited_urls

    print(f"Scraping page {current_page}")
    print(f"Page URL: {search_url}")
    soup_search = get_soup(search_url)
    link_elements = soup_search.select("[data-asin] h2 a")
    page_data = []

    for link in link_elements:
        if current_link >= max_links:
            print(f"Reached limit of {max_links} links.")
            return page_data

        full_url = urljoin(search_url, link.attrs.get("href"))
        if full_url not in visited_urls:
            visited_urls.add(full_url)
            print("---------------------------------------------------------------")
            print(f"Link count: {current_link + 1}")
            product_info = get_product_info(full_url, search_url)
            if product_info:
                # Insert to MongoDB.
                operation = UpdateOne({"ASIN": product_info["ASIN"]}, {"$set": product_info}, upsert=True)
                result = col.bulk_write([operation])
                if result.upserted_count:
                    print(f"Insert new document.")
                else:
                    print(f"Update existing document.")
                current_link += 1

    # If we haven't reached the max links and there is a next page, scrape the next page
    if current_link < max_links:
        next_page_el = soup_search.select_one('a.s-pagination-next')
        if next_page_el and current_page < max_pages:
            next_page_url = next_page_el.attrs.get('href')
            next_page_url = urljoin(search_url, next_page_url)
            page_data += parse_listing(next_page_url, max_links, current_link, max_pages, current_page + 1)

    return page_data


def main():
    search_url = generate_amazon_search_url(category, keyword)
    data = []
    data = parse_listing(search_url, max_links)
    df = pd.DataFrame(data)
    df.to_csv("amazon_product_scraper_results.csv")


if __name__ == '__main__':
    main()
