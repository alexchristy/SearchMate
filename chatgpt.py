import os
import openai
import logging
import json
from urllib.request import urlopen
from utils import num_tokens_from_string, divide_and_round_up, chunk_array

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

    def get_greeting(self):
        '''
        This function queries the GPT-3.5-Turbo model for a greeting.
        '''

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "user",
                "content": "Can you generate me a simple short greeting someone who is looking for something. Just give me a greeting no quotes of any kind."
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
    
    def get_welcome_back(self):
        '''
        This function queries the GPT-3.5-Turbo model for a greeting.
        '''

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "user",
                "content": "Can you generate me a simple, short, and concise welcome back message. Just give me the welcome back message no quotes of any kind."
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

    def get_search_queries(self, user_query:str, base_url:str):

        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
            "role": "user",
            "content": f"You are a Google search expert, capable of generating the most precise and relevant search queries. I have a task for you that involves analyzing a user's search intent on a specific website. The user could be searching for a variety of things: a product, a location, or specific information available on that site. Here's how I'd like you to approach this:\n\n    Contextual Analysis: Take a moment to understand the User Query and the User URL. These are placeholders that will be filled in later. Consider what the user might be looking for based on the website they are currently on.\n\n    Search Query Generation: Use your expertise to craft the most effective Google search queries that would yield the most relevant results for the user's intent. Think about using site-specific keywords, filters, or other advanced Google search techniques.\n\n    Output: Return the Google search queries you've generated as a Python list. The list should only contain the search strings, nothing else.\n\n    Assumptions: Don't worry about the possibility that the user might be searching for something that doesn't exist. Your task is to generate the best possible search queries based on the given context.\n\nReference Material:\n\n    User Query: {user_query}\n    User URL: {base_url}\n\nPlease proceed with this task and ONLY return the Python list of the best three Google search queries. ONLY the Python list of the best three Google search queries. Nothing else."
            }
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
        
        message = response['choices'][0]['message']['content']
        query_list = json.loads(message)
        return query_list
    
    def get_relevant_result(self, user_query: str, base_url: str, search_results: list):
        '''
        This function queries the GPT-4 model for a relevant result.
        '''

        message_to_send = [
                {
                "role": "user",
                "content": f"As the world's best intention predictor, I am seeking your expertise to analyze the provided data and select the most suitable and precise outcome for the user's query. The user's query refers to their specific search request on the website they are currently browsing. The User URL indicates the website that the user was on when they made the query, and it is essential to consider this context throughout the process. Your task is to examine the user's query, taking into account the website's context, and evaluate the search results obtained from Google. Pay close attention to the title and snippet, as they provide a glimpse into the content of each result. Additionally, verify that the link corresponds to the same site the user searched from. If there is no relevant result return None. Your final task is to provide only the link to the most relevant search result. Remember return only the link.\n\nUser Query: {user_query}\nUser URL: {base_url}"
                }
            ]

        for i, result in enumerate(search_results):  # Changed to iterate over list of dictionaries

            link = result.get('link')  # Using .get() for safer dictionary access
            if link is None:
                continue

            result_title = result.get('title')
            if result_title is None:
                continue

            snippet = result.get('snippet')
            if snippet is None:
                continue

            result_message = {
                "role": "user",
                "content": f"Result {i + 1}:\nTitle: {result_title}\nLink: {link}\nSnippet: {snippet}"
                }

            message_to_send.append(result_message)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message_to_send,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        relevant_link = response['choices'][0]['message']['content']

        return relevant_link
