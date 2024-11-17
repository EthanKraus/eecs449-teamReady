from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.amazon_search_scraper import search_scraping

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint working!"})

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Get the GPT-extracted parameters
        data = request.json
        print("Received GPT-extracted parameters:", data)  # Debug print
        
        # Extract parameters from GPT's JSON format
        category = data.get('category')
        keyword = data.get('keyword')  # From 'keywords' in GPT response
        max_links_num = data.get('max_links_num', 10)
        
        # Generate Amazon search URL
        search_url = f"https://www.amazon.com/s?k={keyword}&i={category}"
        print(f"Generated search URL: {search_url}")  # Debug print
        
        # Call the scraper
        results = search_scraping(
            search_url=search_url,
            category=category,
            keyword=keyword,
            max_links_num=max_links_num
        )
        
        return jsonify({
            "status": "success",
            "results": results,
            "message": f"Found {len(results)} products"
        })
        
    except Exception as e:
        print(f"Error in scraper endpoint: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Error processing request"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000) 