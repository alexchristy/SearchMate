from flask import Flask, jsonify, request
import logging
from web_utils import get_sitemap_url, is_valid_url, get_sitemaps, fetch_sitemap_contents
from utils import is_valid_query, is_all_none, load_environment
from chatgpt import GPT4

# Initialize Logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

app = Flask(__name__)

load_environment()

# Initialize GPT4
gpt4 = GPT4()

@app.route('/find/page', methods=['POST'])
def find_page():
    try:
        # Parse JSON data from the request
        data = request.json

        url = data.get('url', None)
        query = data.get('query', None)

        if url is None:
            return jsonify({'error': 'Missing url parameter.'}), 401
        
        if query is None:
            return jsonify({'error': 'Missing query parameter.'}), 402

        # Log the received data
        logging.info(f"Received url: {url}, query: {query}")

        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL.'}), 421
        
        if not is_valid_query(query):
            return jsonify({'error': 'Invalid query.'}), 422
        
        # Extract the sitemap URL from the base URL
        base_sitemap_url = get_sitemap_url(url)

        # Get the sitemaps from the sitemap URL
        sitemaps = get_sitemaps(base_sitemap_url)

        if not sitemaps:
            return jsonify({'error': 'No sitemaps found.'}), 423
        
        # Filter for the relevant sitemaps
        sitemaps = gpt4.get_relevant_sitemaps(sitemaps, query)

        sitemap_contents = fetch_sitemap_contents(sitemaps)

        if is_all_none(sitemap_contents):
            return jsonify({'error': 'No sitemap contents found.'}), 424
        
        if not sitemap_contents:
            return jsonify({'error': 'No sitemap contents found.'}), 424

        

        return jsonify({'message': 'Data received'}), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/responses/greeting', methods=['GET'])
def greeting():
    try:
        message = gpt4.get_greeting()
        return jsonify({'message': message}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='10.167.0.100', port=5000)