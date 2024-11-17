from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.amazon_search_scraper import search_scraping
from urllib.parse import quote_plus

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
        keywords = data.get('keyword', [])  # Match the frontend's 'keyword' parameter
        max_links_num = data.get('max_links_num', 10)
        
        # Debug logging
        print(f"Category: {category}")
        print(f"Keywords: {keywords}")
        print(f"Max links: {max_links_num}")
        
        search_term = ' '.join(keywords) if isinstance(keywords, list) else str(keywords)
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

if __name__ == '__main__':
    app.run(debug=True, port=8000) 