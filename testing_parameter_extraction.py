import openai

def extract_search_params(user_query):
    response = openai.Completion.create(
        model="text-davinci-003",  # Or another suitable model
        prompt=f"Extract keywords, category, and search limit from the following query: '{user_query}'. Format as JSON. Example: {{'keywords': '', 'category': '', 'limit': 0}}.",
        max_tokens=50,
        temperature=0
    )
    return response['choices'][0]['text']

# Example user query
user_query = "Find 5 smart home devices"
params = extract_search_params(user_query)
print(params)
