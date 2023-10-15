import os
import logging
import requests
import json

class GoogleSearch:
    def __init__(self, api_key=None, search_engine_id=None):
        """
        Initialize GoogleSearch class.
        
        Parameters:
        - api_key (str): Google Custom Search API key. If None, falls back to environment variable.
        - search_engine_id (str): Google Custom Search Engine ID. If None, falls back to environment variable.
        """
        self.api_key = api_key if api_key else os.getenv("GOOGLE_SEARCH_API_KEY")
        self.search_engine_id = search_engine_id if search_engine_id else os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        
        # Fallback to environment variables if either api_key or search_engine_id is not provided
        if self.api_key is None:
            logging.warning("Google Custom Search API Key not provided, attempting to use environment variable.")
        
        if self.search_engine_id is None:
            logging.warning("Google Custom Search Engine ID not provided, attempting to use environment variable.")
    
    def search(self, query):
        """
        Perform a Google search using the initialized API key and search engine ID.
        
        Parameters:
        - query (str): The search query.
        
        Returns:
        - dict: Search results.
        """
        # Construct the API URL
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx={self.search_engine_id}"
        
        # Perform the HTTP request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            logging.error(f"Failed to perform search. HTTP Status Code: {response.status_code}")
            return None
        
    def get_top_result(self, query):
        """
        Perform a Google search and return the highest-ranked result with its info.

        Parameters:
        - query (str): The search query.

        Returns:
        - dict: A dictionary containing the title, link, and snippet of the top result,
                or None if search fails or no items are found.
        """
        search_results = self.search(query)
        
        if search_results:
            items = search_results.get("items", [])
            if items:
                top_result = {
                    "title": items[0].get("title", "Unknown"),
                    "link": items[0].get("link", "Unknown"),
                    "snippet": items[0].get("snippet", "Unknown")
                }
                return top_result
            else:
                logging.warning(f"No search results found for query: {query}")
                return None
        else:
            logging.error(f"Search failed for query: {query}")
            return None
