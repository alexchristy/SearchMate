import requests
import logging
from urllib.parse import urlparse
import validators
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to extract the base URL from a given link
def get_base_url(link):
    try:
        parsed_url = urlparse(link)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return base_url
    except Exception as e:
        logger.error(f"Error extracting base URL: {str(e)}")
        return None

def is_valid_url(url):
    if validators.url(url):
        return True
    else:
        return False
    
def fetch_page_content(url):
    """
    Fetch the page content of a given URL and returns its text content for summary.
    Handles both paragraph-heavy and tag-specific pages like shopping sites.
    """
    try:
        # Fetch the page content using requests
        response = requests.get(url=url, timeout=3)
        
        # Raise an error if status code indicates failure
        response.raise_for_status()
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to get text from paragraphs first
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs])
        
        # If little to no text is found in paragraphs, fetch text from other tags
        if len(text_content.split()) < 50:
            additional_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'li', 'a', 'span', 'div']
            additional_text = " ".join([tag.get_text() for tag_name in additional_tags for tag in soup.find_all(tag_name)])
            text_content += " " + additional_text
            
        return text_content.strip()
    
    except RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None