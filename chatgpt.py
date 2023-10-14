import os
import openai
import logging
import json
from backoff import on_exception, expo
from utils import num_tokens_from_string, divide_and_round_up

class GPT4:
    def __init__(self, api_key=None):
        """
        Initialize GPT3TurboDestinationAnalysis class.
        
        Parameters:
        - api_key (str): OpenAI API key. If None, falls back to environment variable.
        """
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        
        # Fallback to environment variable if api_key is not provided
        if self.api_key is None:
            logging.warning("OpenAI API Key not provided, attempting to use environment variable.")
        
        openai.api_key = self.api_key

    def get_relevant_link_from_sitemap(sitemap_contents, query):
        """
        Get the relevant link from the sitemap contents.
        
        Parameters:
        - sitemap_contents (list): List of sitemap contents.
        - query (str): Query to search for.
        
        Returns:
        - relevant_link (str): Relevant link.
        """

        num_tokens = num_tokens_from_string(query)

        xml_chunks = divide_and_round_up(num_tokens, 8000)

        messages = []


    def get_greeting(self):
        '''
        This function queries the GPT-4 model for a greeting.
        '''

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "user",
                "content": "Can you generate me a simple short greeting someone who is looking for something. Just give me a greeting."
                }
            ],
            temperature=1.5,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        message = response['choices'][0]['message']['content']
        return message
    
    @on_exception(expo, openai.OpenAIError, max_tries=5)
    def call_get_relevant_sitemaps(self, sitemaps, query):
        """
        Separate API call to OpenAI in a different function for better retry mechanism.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                "role": "user",
                "content": f"Look at the list of site maps and choose the three that are most relevant to the user query below. If there are three or less sitemaps, return all three. Return them in a Python list from most relevant to least relevant.\n\nUser Query: {query}\nSitemaps: {sitemaps}"
                }
            ],
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response

    def get_relevant_sitemaps(self, sitemaps, query):
        """
        Get the relevant sitemaps from the list of sitemaps.
        """
        try:
            response = self.call_get_relevant_sitemaps(sitemaps, query)
            message = response['choices'][0]['message']['content']
            json_compatible_string = message.replace("'", '"')
            parsed_list = json.loads(json_compatible_string)
            logging.info(f'Parsed list: {parsed_list}')
            return parsed_list
        except json.JSONDecodeError as e:
            logging.error(f'Error decoding JSON: {e}')
            return []
        except openai.OpenAIError as e:
            logging.error(f"GPT4 error: {e}")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return []
