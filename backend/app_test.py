import requests
import json

def test_frontend_flow():
    base_url = 'http://localhost:8000'
    
    # Test cases simulating GPT-extracted JSON from frontend
    test_cases = [
        {
            "description": "User asks: 'I'm looking for a red dress under $100'",
            "gpt_extracted_json": {
                "category": "fashion",
                "keywords": "red dress",  # Note: GPT returns 'keywords'
                "max_limit": "100"
            },
            "scraper_params": {
                "category": "fashion",
                "keyword": "red dress",  # Note: Scraper expects 'keyword'
                "max_links_num": 10
            }
        },
        {
            "description": "User asks: 'Can you find gaming laptops under $2000?'",
            "gpt_extracted_json": {
                "category": "electronics",
                "keywords": "gaming laptop",
                "max_limit": "2000"
            },
            "scraper_params": {
                "category": "electronics",
                "keyword": "gaming laptop",
                "max_links_num": 10
            }
        }
    ]

    print("Testing Frontend → Backend → Scraper Flow\n")

    for case in test_cases:
        print(f"\nTest Case: {case['description']}")
        print(f"GPT Extracted JSON: {json.dumps(case['gpt_extracted_json'], indent=2)}")
        
        try:
            # Call scraper endpoint with GPT-extracted parameters
            response = requests.post(
                f"{base_url}/scrape",
                json=case['scraper_params'],
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"\nBackend Response:")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                results = response.json()
                print(f"Success: {results.get('message')}")
                
                # Show example product
                if results.get('results'):
                    print("\nExample Product:")
                    print(json.dumps(results['results'][0], indent=2))
                    
                    # Verify price limit if specified
                    if case['gpt_extracted_json'].get('max_limit'):
                        price_limit = float(case['gpt_extracted_json']['max_limit'])
                        product_price = results['results'][0].get('price')
                        if product_price and product_price > price_limit:
                            print(f"⚠️ Warning: Product price (${product_price}) exceeds limit (${price_limit})")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    test_frontend_flow()
