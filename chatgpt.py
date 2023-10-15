import os
import openai
import logging
import json
from web_utils import fetch_page_content
from utils import num_tokens_from_string, divide_and_round_up, extract_first_url

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
            "content": f"You are a Google search expert, capable of generating the most precise and relevant search queries. I have a task for you that involves analyzing a user's search intent on a specific website. The user could be searching for a variety of things: a product, a location, or specific information available on that site. Here's how I'd like you to approach this:\n\n    Contextual Analysis: Take a moment to understand the User Query and the User URL. These are placeholders that will be filled in later. Consider what the user might be looking for based on the website they are currently on.\n\n    Search Query Generation: Use your expertise to craft the most effective Google search queries that would yield the most relevant results for the user's intent. Think about using site-specific keywords, filters, or other advanced Google search techniques.\n\n    Output: Return the Google search queries you've generated as a Python list. The list should only contain the search strings, nothing else.\n\n    Assumptions: Don't worry about the possibility that the user might be searching for something that doesn't exist. Your task is to generate the best possible search queries based on the given context and in the native language of the user.\n\nReference Material:\n\n    User Query: {user_query}\n    User URL: {base_url}\n\nPlease proceed with this task and ONLY return the Python list of the best three Google search queries. ONLY the Python list of the best three Google search queries. Nothing else."
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

        relevant_link = extract_first_url(relevant_link)

        return relevant_link
    
    def is_user_searching(self, user_query: str, base_url: str):

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                "role": "user",
                "content": f"I am seeking your expertise in analyzing a user's search intent on a specific website. Your exceptional ability to discern intentions makes you the best person for this task. The user's search could encompass various aspects such as a product, a location, or specific information available on the website. To aid you in making an accurate determination, I will provide you with the following information: the User Query, which represents what the user is saying or desiring, and the User URL, which indicates the current site the user is on. Your objective for this task is to examine the user query and user URL and ascertain whether the user is searching for a product, a location, or specific information available on that site. If it is evident that the user is searching for something, please return True. Conversely, if it seems that the user is not searching for anything, please return False. Please refrain from returning any other information beyond these outcomes.\n\nUser Query: {user_query}\nUser URL: {base_url}"
                }
            ],
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        message = response['choices'][0]['message']['content']

        if message == 'True':
            return True
        
        if message == 'False':
            return False
        
        logging.info(f"Unexpected response from GPT-4: {message}")
        return None

    def gen_customer_response(self, user_query: str, base_url: str, relevant_link: str, page_content: str):

        if page_content is None:
            logging.info("No page content in customer_response(). Using generic response.")
            page_content = "(empty)"
        
        page_num_tokens = num_tokens_from_string(page_content)

        if page_num_tokens > 7800:
            logging.info(f"Page content is too long ({page_num_tokens} tokens), truncating to 7800 tokens.")
            chunks = divide_and_round_up(page_num_tokens, 7800)

            end_index = page_num_tokens / chunks
            end_index = int(end_index)

            page_content = page_content[:end_index]


        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                "role": "user",
                "content": f"As the best salesperson on the planet, your exceptional skills are needed to analyze the provided data and generate a response. The data consists of three components: User Query, User URL, and Page Content. User Query refers to the search term entered by the user on the website, while User URL is the website they were on when making that query. Page Content represents the relevant text on the page related to the user's query. The relevant link is the link to the page where the Page Content came from. The relevant link is the page that most matches what the user was looking for.\\n\\nYour first task is to determine whether the user was seeking to make a purchase, whether it be a product or a service. If the user was indeed looking for a purchasable item, your objective is to subtly sell them a product, just like a professional salesperson would. This requires carefully examining their query and providing a concise and clear summary of the page content that directly addresses their query. You can find details in the Page Content. Additionally, you should highlight any relevant information and details about the product that may persuade them to make a purchase. The aim is to subtly guide them towards the product or service they are seeking.\\n\\nHowever, if the user's search does not indicate an intention to purchase, your response should focus on concisely summarizing the page content and addressing their specific query. Your goal is to provide them with a clear and comprehensive answer to what they were searching for, without attempting to sell them anything.\\n\\nPlease provide only the response that you would give to the customer based on the above instructions. If Page Content is empty or None craft a response similarly but make it relevant to the User Query wihtout mentioning you do not have details or page content. You are directly communicating to the customer. Only give the response to the customer. Call the user query a question only. Keep it short and concise and not very technical. Max 3 concise sentences. Repond is user's native language.\n\nUser Query: {user_query}\nUser URL: {base_url}\nRelevant Link: {relevant_link}\nPage Content: {page_content}"
                }
            ],
            temperature=0.25,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        message = response['choices'][0]['message']['content']

        return message
    
    def gen_unfocused_response(self, user_query: str, base_url: str):

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                "role": "user",
                "content": f"You are an expert at social interaction and communication. Using your skills, I need you to respond to the User Query and ask them if there is anything you can help them find on the website pointed at by User URL. User query below is the query the user sent to us and the User URL is the current site they are at when the sent query. Keep it simple and short and concise. Max 2 sentences. Make sure it makes sure it responds to the user query and asks them if they need help. Only give the response to the user.\n\nUser Query: {user_query}\nUser URL: {base_url}"
                }
            ],
            temperature=0.25,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        message = response['choices'][0]['message']['content']

        return message

        