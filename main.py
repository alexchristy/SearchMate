from flask import Flask, jsonify, request
import logging
from web_utils import is_valid_url, get_base_url
from utils import is_valid_query, load_environment
from chatgpt import GPT4
from googlesearch import GoogleSearch
import json
from web_utils import fetch_page_content

# Initialize Logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

app = Flask(__name__)

load_environment()

# Initialize GPT4
gpt4 = GPT4()
google_seach = GoogleSearch()

@app.route('/find/page', methods=['POST'])
def find_page():
    try:
        # Parse JSON data from the request
        data = request.json

        url = data.get('url', None)
        query = data.get('query', None)

        query = query.lower()

        if url is None:
            return jsonify({'error': 'Missing url parameter.'}), 401
        
        if query is None:
            return jsonify({'error': 'Missing query parameter.'}), 402

        # Log the received data
        logging.info(f"Received url: {url}, query: {query}")

        if not is_valid_url(url):
            url = "https://www.google.com"
        
        if not is_valid_query(query):
            return jsonify({'error': 'Invalid query.'}), 422
        
        is_user_searching = gpt4.is_user_searching(query, url)
        is_user_shopping = gpt4.is_user_shopping(query, url)

        if not is_user_searching:
            logging.info(f"User is not searching for the given query: {query}")
            
            unfocused_response = gpt4.gen_unfocused_response(query, url)

            return jsonify({'link': None, 'message': unfocused_response}), 200
        
        if is_user_searching is None:
            return jsonify({'error': 'An error occurred.'}), 500

        # Extract the base URL from the given URL
        base_url = get_base_url(url)

        retries = 1
        while retries >= 0:
            search_queries = gpt4.get_search_queries(query, base_url)

            results = set()
            unique_results_list = []
            for search in search_queries:
                current_result = google_seach.get_top_result(search)

                if current_result is None:
                    continue
                
                result_str = json.dumps(current_result)

                results.add(result_str)
                unique_results_list = [json.loads(x) for x in results]

            if len(unique_results_list) <= 0:
                base_url = "https://www.google.com"
                retries -= 1

            break
        
        if len(unique_results_list) <= 0:
            return jsonify({'link': None, 'message': 'Sorry I was not able to find any results.'}), 200
        
        page_content = None
        for result in unique_results_list:
            relevant_link = gpt4.get_relevant_result(query, base_url, unique_results_list)

            page_content = fetch_page_content(relevant_link)

            if is_user_shopping:
                relevant_product_link = gpt4.get_relevant_product_link(query, base_url, unique_results_list)

            # If successful, break out of the loop
            if page_content is not None:
                break

            unique_results_list.remove(result)

        if relevant_link == 'None' or relevant_link is None:
            return jsonify({'link': None, 'message': 'Sorry I was not able to find any relevant links or pages for you.'}), 200

        if is_user_shopping and (relevant_product_link is None or relevant_product_link == 'None'):
            relevant_product_link = relevant_link

        is_page_empty = gpt4.is_page_empty(page_content)

        if is_page_empty is None:
            logging.info('Error occurred while checking if page is empty.')
            return jsonify({'error': 'An error occurred.'}), 500
        
        if is_user_shopping:
            customer_response = gpt4.gen_customer_response(query, base_url, relevant_product_link, page_content)
        else:
            customer_response = gpt4.gen_customer_response(query, base_url, relevant_link, page_content)

        if is_page_empty:
            logging.info('Page is empty.')
            return jsonify({'link': None, 'message': customer_response}), 200
        
        return jsonify({"link": relevant_link, "message": customer_response}), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/responses/greeting', methods=['POST'])
def greeting():
    try:
        # Parse JSON data from the request
        data = request.json

        url = data.get('url', None)

        if url is None:
            return jsonify({'error': 'Missing url parameter.'}), 401

        message = gpt4.get_greeting(url)
        return jsonify({'message': message}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/responses/welcome-back', methods=['POST'])
def welcome_back():
    try:
        # Parse JSON data from the request
        data = request.json

        url = data.get('url', None)

        if url is None:
            return jsonify({'error': 'Missing url parameter.'}), 401

        message = gpt4.get_welcome_back(url)
        return jsonify({'message': message}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='10.167.0.100', port=5000)