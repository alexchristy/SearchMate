from flask import Flask, jsonify, request
import logging

# Initialize Logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

app = Flask(__name__)

@app.route('/find/page', methods=['POST'])
def find_page():
    try:
        # Parse JSON data from the request
        data = request.json

        url = data.get('url', None)
        query = data.get('query', None)

        if url is None:
            return jsonify({'error': 'Missing url parameter.'}), 400
        
        if query is None:
            return jsonify({'error': 'Missing query parameter.'}), 400

        # Log the received data
        logging.info(f"Received url: {url}, query: {query}")

        

        return jsonify({'message': 'Data received'}), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)