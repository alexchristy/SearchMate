import logging
from dotenv import load_dotenv
import tiktoken
import math

def is_valid_query(query):
    """
    Validates whether a string is a valid query by applying a series of checks using if statements.

    Args:
        query (str): The string to validate.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    if query is None:
        return False

    if not query.strip():
        return False

    # Additional checks can be added here using more if statements

    return True

def is_all_none(arr):
    return all(element is None for element in arr)

def load_environment(file_path=".env"):
    """
    Load environment variables using python-dotenv.

    :param file_path: Path to the .env file
    :type file_path: str
    """
    # Load the .env file
    if load_dotenv(dotenv_path=file_path):
        logging.info("Successfully loaded environment variables from .env file.")
    else:
        logging.error(f"Failed to load .env file from {file_path}")

def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def divide_and_round_up(dividend, divisor):
    result = math.ceil(dividend / divisor)
    return result