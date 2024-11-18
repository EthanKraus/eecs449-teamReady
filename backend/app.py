from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.amazon_search_scraper import search_scraping
from urllib.parse import quote_plus
import scraper.amazon_product_scraper as ps
import openai
import os

# Remove dotenv and directly set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint working!"})

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        print("Received GPT-extracted parameters:", data)
        
        category = data.get('category')
        keyword = data.get('keyword')
        max_links_num = data.get('max_links_num', 10)
        
        # Debug logging
        print(f"Category: {category}")
        print(f"Keyword: {keyword}")
        print(f"Max links: {max_links_num}")
        
        search_term = str(keyword)
        print(f"Search term: {search_term}")
        
        # URL encode the search terms
        encoded_search = quote_plus(search_term)
        encoded_category = quote_plus(category)
        search_url = f"https://www.amazon.com/s?k={encoded_search}&i={encoded_category}"
        print(f"Generated search URL: {search_url}")
        
        results = search_scraping(
            search_url=search_url,
            category=category,
            keyword=search_term,
            max_links_num=max_links_num
        )
        
        print(f"Scraping results: {results}")  # Debug the results
        
        if not results:
            print("No results returned from scraper")
            return jsonify({
                "status": "success",
                "results": [],
                "message": "No products found"
            })
        
        return jsonify({
            "status": "success",
            "results": results,
            "message": f"Found {len(results)} products"
        })
        
    except Exception as e:
        print(f"Error in scraper endpoint: {str(e)}")
        import traceback
        print(traceback.format_exc())  # Print full stack trace
        return jsonify({
            "error": str(e),
            "message": "Error processing request"
        }), 500

def get_summary_from_openai(reviews_text):
    """
    Calls the OpenAI API to generate a summary from the given text.
    """
    if not reviews_text:
        raise ValueError("No review text provided")
        
    try:
        print("Calling OpenAI API with text length:", len(reviews_text))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes product reviews."},
                {"role": "user", "content": f"Summarize these customer reviews into a one-paragraph overall review:\n{reviews_text}"}
            ],
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            n=1,
            stop=None
        )
        
        if not response.choices:
            raise ValueError("No response choices returned from OpenAI")
            
        summary = response.choices[0]['message']['content'].strip()
        if not summary:
            raise ValueError("Empty summary returned from OpenAI")
            
        return summary
        
    except Exception as e:
        print(f"Detailed OpenAI API Error: {str(e)}")
        import traceback
        print("OpenAI API Error Traceback:", traceback.format_exc())
        raise  # Re-raise the error for the main handler

@app.route('/scrape_summary', methods=['POST'])
def scrape_summary():
    try:
        data = request.json
        print("Received review request with data:", data)
        
        if not data or 'ASIN' not in data:
            return jsonify({
                "error": "Missing ASIN",
                "message": "Product ASIN is required"
            }), 400
            
        ASIN = data['ASIN']
        print(f"Processing review request for ASIN: {ASIN}")
        
        results = ps.get_product_info(ASIN=ASIN)
        
        if not results:
            return jsonify({
                "error": "No product found",
                "message": f"Could not find product with ASIN: {ASIN}"
            }), 404
            
        if 'reviews' not in results or not results['reviews']:
            return jsonify({
                "error": "No reviews found",
                "message": f"No reviews available for product with ASIN: {ASIN}"
            }), 404
            
        reviews_text = " ".join([review.get('reviewText', '') for review in results['reviews']])
        summary = get_summary_from_openai(reviews_text)
        
        return jsonify({
            "status": "success",
            "results": summary,
            "message": f"Successfully generated summary for ASIN: {ASIN}"
        })
        
    except Exception as e:
        print(f"Error processing review request: {str(e)}")
        import traceback
        print("Full traceback:", traceback.format_exc())
        return jsonify({
            "error": str(e),
            "message": "Error processing review request",
            "details": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000) 